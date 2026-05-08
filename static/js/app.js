(function () {
  const savedTheme = localStorage.getItem('smartSpendTheme');
  if (savedTheme === 'dark' || savedTheme === 'light') {
    document.documentElement.dataset.theme = savedTheme;
  }

  const readJson = (id, fallback) => {
    const node = document.getElementById(id);
    if (!node) return fallback;
    try { return JSON.parse(node.textContent); } catch { return fallback; }
  };

  const palette = () => readJson('chart-palette', ['#8CC8FF', '#A6D672', '#FFC6C6', '#9B8CFF']);
  const labels = () => readJson('category-labels', []);
  const values = () => readJson('category-values', []);
  const lineLabels = () => readJson('line-labels', []);
  const lineValues = () => readJson('line-values', []);
  const themeText = () => getComputedStyle(document.documentElement).getPropertyValue('--dark').trim() || '#1B1B1B';
  const themeGrid = () => document.documentElement.dataset.theme === 'dark' ? 'rgba(140,200,255,.16)' : 'rgba(27,27,27,.08)';

  function makeChart(id, type, data, options = {}) {
    const canvas = document.getElementById(id);
    if (!canvas || !window.Chart) return;
    const textColor = themeText();
    return new Chart(canvas, {
      type,
      data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 1200, easing: 'easeOutQuart' },
        plugins: { legend: { labels: { usePointStyle: true, boxWidth: 8, color: textColor } } },
        scales: type === 'doughnut' || type === 'pie' ? {} : {
          y: { beginAtZero: true, grid: { color: themeGrid() }, ticks: { color: textColor } },
          x: { grid: { display: false }, ticks: { color: textColor } },
        },
        ...options,
      },
    });
  }

  window.SmartCharts = {
    dashboard() {
      makeChart('dashboardDonut', 'doughnut', {
        labels: labels(),
        datasets: [{ data: values(), backgroundColor: palette(), borderWidth: 0, hoverOffset: 10 }],
      }, { cutout: '72%' });
    },
    analytics() {
      const colors = palette();
      makeChart('donutChart', 'doughnut', { labels: labels(), datasets: [{ data: values(), backgroundColor: colors, borderWidth: 0, hoverOffset: 12 }] }, { cutout: '68%' });
      makeChart('pieChart', 'pie', { labels: labels(), datasets: [{ data: values(), backgroundColor: colors, borderWidth: 0 }] });
      makeChart('lineChart', 'line', {
        labels: lineLabels(),
        datasets: [{ label: 'Daily spending', data: lineValues(), borderColor: '#9B8CFF', backgroundColor: 'rgba(155,140,255,.18)', tension: .42, fill: true, pointRadius: 5, pointBackgroundColor: '#8CC8FF' }],
      });
      makeChart('barChart', 'bar', {
        labels: labels(),
        datasets: [{ label: 'By category', data: values(), backgroundColor: colors, borderRadius: 18, borderSkipped: false }],
      });
    },
  };

  function animateCounters() {
    document.querySelectorAll('.counter').forEach((node) => {
      const target = Number.parseFloat(node.dataset.target || '0');
      if (!window.gsap) { node.textContent = target.toFixed(0); return; }
      const state = { value: 0 };
      gsap.to(state, {
        value: target,
        duration: 1.3,
        ease: 'power3.out',
        onUpdate: () => { node.textContent = Math.round(state.value).toLocaleString('en-IN'); },
      });
    });
  }

  function initPrediction() {
    const title = document.getElementById('id_title');
    const category = document.getElementById('id_category');
    const chip = document.getElementById('aiPrediction');
    if (!title || !category || !chip) return;
    const rules = [
      { words: ['pizza', 'burger', 'coffee', 'grocery', 'swiggy', 'zomato'], category: 'Food' },
      { words: ['uber', 'ola', 'cab', 'metro', 'bus', 'train'], category: 'Travel' },
      { words: ['netflix', 'prime', 'movie', 'spotify', 'game'], category: 'Entertainment' },
      { words: ['shirt', 'shoe', 'mall', 'amazon'], category: 'Shopping' },
      { words: ['electricity', 'rent', 'wifi', 'phone'], category: 'Bills' },
    ];
    title.addEventListener('input', () => {
      const text = title.value.toLowerCase();
      const match = rules.find((rule) => rule.words.some((word) => text.includes(word)));
      const suggestion = match ? match.category : 'Other';
      chip.textContent = `AI Suggested: ${suggestion}`;
      if (match) category.value = suggestion;
      chip.animate([{ transform: 'scale(.96)' }, { transform: 'scale(1.04)' }, { transform: 'scale(1)' }], { duration: 260 });
    });
  }

  function initThemeToggle() {
    document.querySelectorAll('.theme-toggle').forEach((button) => {
      button.addEventListener('click', () => {
        const root = document.documentElement;
        root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('smartSpendTheme', root.dataset.theme);
        refreshChartsForTheme();
      });
    });
  }

  function refreshChartsForTheme() {
    if (!window.Chart) return;
    const textColor = themeText();
    Object.values(Chart.instances || {}).forEach((chart) => {
      if (chart.options.plugins?.legend?.labels) chart.options.plugins.legend.labels.color = textColor;
      Object.values(chart.options.scales || {}).forEach((scale) => {
        if (scale.ticks) scale.ticks.color = textColor;
        if (scale.grid) scale.grid.color = themeGrid();
      });
      chart.update('none');
    });
  }

  function initMascotSubmit() {
    document.querySelectorAll('.expense-smart-form').forEach((form) => {
      form.addEventListener('submit', (event) => {
        if (form.dataset.celebrated === 'true') return;
        const mascotWrap = form.closest('.panel-card')?.querySelector('.add-mascot-wrap');
        if (!mascotWrap || !window.gsap) return;
        event.preventDefault();
        form.dataset.celebrated = 'true';
        mascotWrap.classList.add('is-celebrating');
        const button = form.querySelector('.mascot-submit');
        if (button) button.textContent = 'Saving...';
        gsap.fromTo(mascotWrap, { scale: 1 }, { scale: 1.04, yoyo: true, repeat: 1, duration: .22, ease: 'power2.out' });
        setTimeout(() => form.submit(), 520);
      });
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    if (window.AOS) AOS.init({ duration: 720, once: true, offset: 40 });
    if (window.lucide) lucide.createIcons();
    animateCounters();
    initPrediction();
    initMascotSubmit();
  });
})();
