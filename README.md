# 复旦人物出生年份分布

本项目爬取复旦大学“复旦百科 — 人物”栏目中的条目，提取人物姓名与出生年份，结果保存为 `data/people.json`，并提供一个前端视图展示按十年分组的出生年份分布（鼠标悬浮显示该组人物名单）。

项目结构
- `scraper.py` — 主爬虫，调用站点内部 API 获取条目列表并抓取详情页以解析出生年份。
- `fix_births.py` — 针对性修复脚本：针对 `birth_year` 为 `2019` / 缺失 / 非法值的条目重抓详情页并尝试提取正确年份。
- `requirements.txt` — Python 依赖（requests, beautifulsoup4 等）。
- `data/people.json` — 爬虫输出的 JSON 数据（项目运行后生成）。
- `frontend/` — 静态前端，包含 `index.html`, `app.js`, `style.css`，使用 Chart.js 绘图。

快速开始（推荐）

1) 创建虚拟环境并安装依赖（建议 Python 3.8+）：

```bash
python -m venv venv
# Windows
venv\Scripts\activate
pip install -r requirements.txt
```

2) 如需使用代理（例如本项目测试时使用的本地代理），在运行示例命令前设置环境变量：

Windows PowerShell:
```powershell
$env:HTTP_PROXY='http://127.0.0.1:7897'
$env:HTTPS_PROXY='http://127.0.0.1:7897'
# 然后运行爬虫
venv\Scripts\python.exe scraper.py
```

3) 运行爬虫生成数据：

```bash
venv\Scripts\python.exe scraper.py
# 输出文件： data/people.json
```

4) 如发现部分条目年份异常（常见误采为条目发布时间，比如 2019），运行修复脚本：

```bash
venv\Scripts\python.exe fix_births.py
# 该脚本会先备份为 data/people.json.bak，然后尝试修正可识别的出生年份
```

5) 启动本地静态服务器查看前端：

```bash
venv\Scripts\python.exe -m http.server 8000
# 在浏览器打开 http://localhost:8000/frontend/
```

数据说明
- 每个条目为 JSON 对象，示例：

```json
{
	"name": "鲍正鹄",
	"birth_year": 1917,
	"url": "http://www.fudan.edu.cn/2019/0426/c427a96253/page.htm"
}
```

- `birth_year` 的提取原则：优先在详情页靠近姓名位置查找模式 `（YYYY—YYYY）`，其次搜索页面中明显的“出生”或年表信息。脚本会校验年份在合理范围（1800—当前年）。

常见问题与调试
- 若看到大量 `birth_year` 为 2019：这是因为站点列表项包含 `publishTime` 字段，早期版本的爬虫可能误用了该字段作为出生年份。已提供 `fix_births.py` 以重抓详情页并优先在详情中提取年份。
- 若爬虫在抓取时长时间挂起或失败，请检查网络/代理设置并增加超时或重试参数（`scraper.py` 与 `fix_births.py` 已包含短超时与重试策略）。
- 网站结构变化：手动打开有问题的条目（`data/people.json` 中的 `url`）检查页面中姓名附近的文本格式，并据此调整 `scraper.py` 中的正则或解析逻辑。

下一步建议（可选）
- 我可以：
	- 批量重新校验所有仍显示为 2019 的条目并自动修正；
	- 为前端添加搜索/筛选和下载 CSV 功能；
	- 将数据存入 SQLite/CSV 以便后续分析。

如需我代为执行上述任一项，请直接回复序号或描述。谢谢！
