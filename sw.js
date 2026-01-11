const CACHE_NAME = 'cografya-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/akarsular.html',
  '/mountains.html',
  '/platolar.html',
  '/tektonikovalar.html',
  '/karstikovalar.html',
  '/deltaovalari.html',
  '/selale.html',
  '/buzullasma.html',
  '/magaralar.html',
  '/tektonikgoller.html',
  '/volkanikgoller.html',
  '/karstikgoller.html',
  '/heyelansetgoller.html',
  '/aluvyalsetgoller.html',
  '/kiyisetgoller.html',
  '/volkaniksetgoller.html',
  '/manifest.json',
  'https://cdn.tailwindcss.com',
  'https://unpkg.com/lucide@latest',
  'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap',
  'https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&display=swap',
  'https://cdn-icons-png.flaticon.com/512/854/854878.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});
