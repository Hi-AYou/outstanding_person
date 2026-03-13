async function loadData(){
  const res = await fetch('/data/people.json');
  const data = await res.json();

  const items = data.filter(d => d.birth_year && Number.isInteger(d.birth_year));
  if(items.length === 0){
    document.getElementById('chart').parentNode.innerHTML = '<p>未找到出生年份数据，请先运行爬虫生成 data/people.json。</p>';
    return;
  }

  const years = items.map(d=>d.birth_year);
  const min = Math.min(...years);
  const max = Math.max(...years);

  const start = Math.floor(min/10)*10;
  const end = Math.ceil((max+1)/10)*10;

  const labels = [];
  const bins = [];
  for(let y=start;y<end;y+=10){
    labels.push(`${y}-${y+9}`);
    bins.push([]);
  }

  items.forEach(d=>{
    const idx = Math.floor((d.birth_year - start)/10);
    if(idx >=0 && idx < bins.length) bins[idx].push(d.name);
  });

  const counts = bins.map(b=>b.length);

  const ctx = document.getElementById('chart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: '人数',
        data: counts,
        backgroundColor: 'rgba(54,162,235,0.6)'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: {
            label: function(ctx){
              const idx = ctx.dataIndex;
              const names = bins[idx];
              if(!names || names.length === 0) return '无数据';
              // 显示所有名字（若过长会被截断）
              return names.join(', ');
            }
          }
        }
      }
    }
  });
}

loadData().catch(err=>{
  console.error(err);
  document.getElementById('chart').parentNode.innerHTML = '<p>加载数据或渲染图表时出错，查看控制台了解详情。</p>';
});
