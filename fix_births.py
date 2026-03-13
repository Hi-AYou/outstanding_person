import os
import json
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'people.json')


def make_session():
    s = requests.Session()
    retries = Retry(total=3, backoff_factor=0.3, status_forcelist=(500,502,503,504))
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.headers.update({'User-Agent': 'Mozilla/5.0 (fix_births script)'})
    return s


def extract_year_near_name(text, name):
    # Prefer pattern like 名字（YYYY—YYYY） near the name
    # Search for a short window around first occurrence of the name
    idx = text.find(name)
    if idx != -1:
        start = max(0, idx - 200)
        end = min(len(text), idx + 200)
        window = text[start:end]
        m = re.search(r'（\s*(\d{4})[—\-]\d{4}', window)
        if m:
            return int(m.group(1))
    # fallback: look for the first year-range in the whole text
    m = re.search(r'（\s*(\d{4})[—\-]\d{4}', text)
    if m:
        return int(m.group(1))
    # explicit '出生' patterns
    m = re.search(r'出生[:：]\s*(\d{4})', text)
    if m:
        return int(m.group(1))
    return None


def valid_year(y):
    return y is not None and 1800 <= y <= datetime.now().year


def main():
    if not os.path.exists(DATA_PATH):
        print('data/people.json not found')
        return

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    backup = DATA_PATH + '.bak'
    with open(backup, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Backup written to', backup)

    sess = make_session()
    updated = 0
    total_check = 0
    for item in data:
        by = item.get('birth_year')
        if by is None or by == 2019 or not valid_year(by):
            total_check += 1
            url = item.get('url')
            name = item.get('name', '').strip()
            if not url or not name:
                continue
            try:
                r = sess.get(url, timeout=8)
                text = ''
                try:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    title = (soup.title.string or '') if soup.title else ''
                    meta_desc = ''
                    md = soup.find('meta', attrs={'name': 'description'})
                    if md and md.get('content'):
                        meta_desc = md['content']
                    body = soup.get_text(separator=' ', strip=True)
                    combined = ' '.join([title, meta_desc, body[:2000]])
                    year = extract_year_near_name(combined, name)
                    if year and valid_year(year):
                        item['birth_year'] = year
                        updated += 1
                        print(f"Updated {name}: {year}")
                    else:
                        print(f"No year found for {name}")
                except Exception as e:
                    print('parse error', url, e)
            except Exception as e:
                print('request error', url, e)
            time.sleep(0.2)

    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'Done. Checked {total_check} entries, updated {updated} entries.')


if __name__ == '__main__':
    main()
