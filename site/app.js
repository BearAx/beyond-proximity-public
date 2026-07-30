const navToggle = document.querySelector('.nav-toggle');
const siteNav = document.querySelector('.site-nav');

const readPath = (value, path) => path.split('.').reduce(
  (current, key) => (current == null ? undefined : current[key]),
  value,
);

const formatMetric = (value, format) => {
  if (typeof value !== 'number') return String(value ?? '');
  if (format === 'percent') return `${value.toFixed(1)}%`;
  if (format === 'integer') return Math.round(value).toLocaleString('en-US');
  if (format === 'decimal-1') return value.toFixed(1);
  if (format === 'decimal-2') return value.toFixed(2);
  if (format === 'decimal-3') return value.toFixed(3);
  if (format === 'seconds') return `${(value / 1000).toFixed(2)} s`;
  return value.toLocaleString('en-US');
};

fetch('data/evidence-summary.json')
  .then((response) => {
    if (!response.ok) throw new Error(`Evidence summary returned ${response.status}`);
    return response.json();
  })
  .then((evidence) => {
    document.querySelectorAll('[data-metric]').forEach((element) => {
      const value = readPath(evidence, element.dataset.metric);
      if (value !== undefined && value !== null) {
        element.textContent = formatMetric(value, element.dataset.format);
      }
    });
  })
  .catch((error) => {
    console.warn('Using checked-in metric fallbacks:', error);
  });

navToggle?.addEventListener('click', () => {
  const open = siteNav.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(open));
});

siteNav?.addEventListener('click', (event) => {
  if (event.target.matches('a')) {
    siteNav.classList.remove('open');
    navToggle?.setAttribute('aria-expanded', 'false');
  }
});

const tabs = [...document.querySelectorAll('[role="tab"]')];
const selectTab = (tab) => {
  tabs.forEach((candidate) => {
    const selected = candidate === tab;
    candidate.setAttribute('aria-selected', String(selected));
    candidate.tabIndex = selected ? 0 : -1;
    document.getElementById(candidate.getAttribute('aria-controls')).hidden = !selected;
  });
};

tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    let nextIndex = index;
    if (event.key === 'ArrowLeft') nextIndex = (index - 1 + tabs.length) % tabs.length;
    if (event.key === 'ArrowRight') nextIndex = (index + 1) % tabs.length;
    if (event.key === 'Home') nextIndex = 0;
    if (event.key === 'End') nextIndex = tabs.length - 1;
    tabs[nextIndex].focus();
    selectTab(tabs[nextIndex]);
  });
});

document.querySelectorAll('[data-copy-target]').forEach((button) => {
  button.addEventListener('click', async () => {
    const target = document.getElementById(button.dataset.copyTarget);
    if (!target) return;
    const original = button.textContent;
    try {
      await navigator.clipboard.writeText(target.innerText);
      button.textContent = 'Copied';
    } catch {
      button.textContent = 'Select text';
    }
    window.setTimeout(() => { button.textContent = original; }, 1600);
  });
});

const dialog = document.getElementById('figure-dialog');
const dialogImage = dialog?.querySelector('img');

document.querySelectorAll('[data-full]').forEach((button) => {
  button.addEventListener('click', () => {
    if (!dialog || !dialogImage) return;
    const preview = button.querySelector('img');
    dialogImage.src = button.dataset.full;
    dialogImage.alt = preview?.alt || 'Full-size research figure';
    dialog.showModal();
  });
});

dialog?.querySelector('.dialog-close')?.addEventListener('click', () => dialog.close());
dialog?.addEventListener('click', (event) => {
  if (event.target === dialog) dialog.close();
});
