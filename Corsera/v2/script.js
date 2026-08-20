const cards = Array.from(document.querySelectorAll('.course-card'));

const activeMap = new Map([
  ['python-everybody', cards[0]],
  ['specialization', cards[1]],
  ['data-science', cards[2]],
  ['data-analysis', cards[3]],
  ['automation', cards[4]],
]);

function setActiveCard(card) {
  cards.forEach((item) => item.classList.remove('active'));
  card.classList.add('active');
  card.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
}

cards.forEach((card) => {
  card.addEventListener('click', () => setActiveCard(card));
});

document.addEventListener('keydown', (event) => {
  if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp') return;

  const activeIndex = cards.findIndex((card) => card.classList.contains('active'));
  const direction = event.key === 'ArrowDown' ? 1 : -1;
  const nextIndex = Math.max(0, Math.min(cards.length - 1, activeIndex + direction));

  setActiveCard(cards[nextIndex]);
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
      }
    });
  },
  { threshold: 0.18 }
);

cards.forEach((card) => observer.observe(card));

