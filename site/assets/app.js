(function () {
  // Меню
  var menu = document.querySelector('.menu');
  var btn = document.querySelector('.menu-btn');
  function setMenu(open) {
    menu.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open);
    btn.textContent = open ? btn.dataset.close : btn.dataset.open;
    document.body.style.overflow = open ? 'hidden' : '';
    document.body.classList.toggle('menu-open', open);
  }
  btn.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });

  // Лайтбокс листает в исходном порядке, поэтому ссылки берём до раскладки по колонкам
  var links = Array.prototype.slice.call(document.querySelectorAll('a[data-lb]'));

  // Галереи: фото идут рядами слева направо, каждое в самую короткую колонку.
  // CSS-колонки шли сверху вниз и перемешивали серии.
  function masonry() {
    var n = window.matchMedia('(max-width: 760px)').matches ? 2 : 3;
    document.querySelectorAll('.gallery:not(.is-grid)').forEach(function (g) {
      if (g._n === n) return;
      g._n = n;
      var tiles = g._tiles || (g._tiles = Array.prototype.slice.call(g.querySelectorAll('.tile')));
      var cols = [], hs = [], k;
      for (k = 0; k < n; k++) { cols.push(document.createElement('div')); cols[k].className = 'gcol'; hs.push(0); }
      tiles.forEach(function (t) {
        var im = t.querySelector('img'), w = im && +im.getAttribute('width'), h = im && +im.getAttribute('height');
        var r = w && h ? h / w : 1, m = 0;
        for (k = 1; k < n; k++) if (hs[k] < hs[m] - .01) m = k;
        cols[m].appendChild(t);
        hs[m] += r + .05;
      });
      g.textContent = '';
      cols.forEach(function (c) { g.appendChild(c); });
      g.classList.add('is-masonry');
    });
  }
  masonry();
  window.addEventListener('resize', masonry);

  // «Обо мне»: цитата по высоте блока «Техника» слева (на телефоне блоки друг под другом, размер из CSS)
  var quote = document.querySelector('.about-quote');
  function fitQuote() {
    if (!quote) return;
    quote.style.fontSize = '';
    if (window.matchMedia('(max-width: 760px)').matches) return;
    var left = quote.parentNode.previousElementSibling, H = left.offsetHeight, lo = 20, hi = 400, m, k;
    for (k = 0; k < 24; k++) {
      m = (lo + hi) / 2; quote.style.fontSize = m + 'px';
      if (quote.offsetHeight > H || quote.scrollWidth > quote.clientWidth + 1) hi = m; else lo = m;
    }
    quote.style.fontSize = lo + 'px';
  }
  fitQuote(); window.addEventListener('resize', fitQuote);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitQuote);

  // Появление при прокрутке
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Главная: заставка, плывущие кадры, имя уходит при прокрутке (по образцу Levitt)
  var home = document.getElementById('home');
  if (home) {
    var stage = home.querySelector('.stage');
    var content = home.querySelector('.home-content');
    var mark = home.querySelector('.wordmark');
    var els = Array.prototype.slice.call(home.querySelectorAll('.drift-item'));
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    var rnd = function (a, b) { return Math.random() * (b - a) + a; };
    var W = 0, H = 0;
    var measure = function () { W = stage.clientWidth; H = stage.clientHeight; };
    measure();
    // Как у Levitt: кадры идут цепочкой с равным шагом в два ряда.
    // Верхний ряд проходит экран за 30 с и идёт под именем, нижний за 40 с и поверх имени.
    // На каждом новом круге кадр получает новую высоту и ширину.
    // Расстановка как в макете Вероники: первая половина кадров (1–5) идёт верхним рядом,
    // остальные (6–9) нижним. При загрузке кадр 1 слева, дальше по порядку вправо.
    var nTop = Math.ceil(els.length / 2), nBot = els.length - nTop;
    var items = els.map(function (el, i) {
      var img = el.querySelector('img');
      var even = i < nTop;
      var k = even ? i : i - nTop, n = even ? nTop : nBot;
      var p0 = even ? .84 - k / n : .82 - k / n;
      var it = { el: el, img: img, dur: even ? 30 : 40, p: ((p0 % 1) + 1) % 1, top: 0, w: 0, end: 0 };
      el.style.zIndex = even ? '' : 200;
      var place = function () {
        var small = W < 800;
        var land = +img.getAttribute('width') > +img.getAttribute('height');
        var add = W < 768 ? 12.5 : W <= 992 ? 10 : 0;   // на узком экране кадры крупнее
        var pct = land ? rnd(20 + add, 30 + add) : rnd(15 + add, 20 + add);
        it.top = even ? (small ? rnd(-2.5, 20) : rnd(-5, 15)) : (small ? rnd(50, 75) : rnd(40, 60));
        el.style.width = pct + '%';
        it.w = W * pct / 100;
        // как у Levitt: от правого края до −25% экрана (на телефоне −40%)
        it.end = W * (small ? .4 : .25);
      };
      it.place = place;
      if (img.complete) place(); else { img.addEventListener('load', function () { place(); draw(); }); place(); }
      return it;
    });
    function draw() {
      items.forEach(function (it) {
        var x = W - (W + it.end) * it.p;
        it.el.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + (it.top / 100 * H).toFixed(1) + 'px,0)';
      });
    }
    draw();
    // Цикл работает только пока кадры плывут: во время прокрутки страницы скрипт ничего не двигает
    var ready = false, moving = false, paused = false, speed = 1, last = 0, raf = 0;
    function tick(now) {
      raf = 0;
      if (paused || !ready || !moving) return;
      var dt = Math.min(now - last, 100) / 1000; last = now;
      items.forEach(function (it) {
        it.p += dt * speed / it.dur;
        if (it.p >= 1) { it.p -= 1; it.place(); }
      });
      draw();
      raf = requestAnimationFrame(tick);
    }
    function start() { if (raf || reduce || paused || !ready || !moving) return; last = performance.now(); raf = requestAnimationFrame(tick); }
    els.forEach(function (el) {
      el.addEventListener('mouseenter', function () { speed = .5; });
      el.addEventListener('mouseleave', function () { speed = 1; });
    });
    var seen = false;
    try { seen = sessionStorage.getItem('splash') === '1'; sessionStorage.setItem('splash', '1'); } catch (err) {}
    // Как у Levitt: обложка уходит, кадры появляются на месте и стоят ещё 1 с, потом плывут
    var go = function () {
      if (ready) return;
      home.classList.add('ready'); ready = true;
      setTimeout(function () { moving = true; start(); }, 1000);
    };
    // Обложка на широком экране: размер не трогаем (кадр заполняет один экран),
    // двигаем только обрезку по вертикали, чтобы глаза не попадали под «Veronika».
    // Вариант a: глаза над именем. Вариант b: глаза ниже «Veronika», на уровне «Kim».
    var EYES = .44;  // где глаза на кадре, доля высоты
    var cv = /[?&]cover=([ab])/.exec(location.search);
    var variant = cv ? cv[1] : 'a';
    var simg = home.querySelector('.splash img');
    function crop() {
      if (!simg || !simg.naturalWidth) return;
      if (window.innerWidth <= 760) { simg.style.objectPosition = ''; return; }
      var sw = stage.clientWidth, sh = stage.clientHeight, nh = mark.offsetHeight;
      var k = Math.max(sw / simg.naturalWidth, sh / simg.naturalHeight);
      var slack = simg.naturalHeight * k - sh;
      if (slack <= 0) { simg.style.objectPosition = ''; return; }
      var target = variant === 'b' ? sh - nh * .27 : (sh - nh) * .55;
      var off = Math.max(0, Math.min(slack, simg.naturalHeight * k * EYES - target));
      simg.style.objectPosition = '50% ' + (off / slack * 100).toFixed(1) + '%';
    }
    if (simg) { if (simg.complete) crop(); else simg.addEventListener('load', crop); }
    // обложка проявляется за 1 с, как у Levitt
    if (simg) { var shown = function () { home.classList.add('cover-in'); }; if (simg.complete) requestAnimationFrame(shown); else { simg.addEventListener('load', shown); simg.addEventListener('error', shown); } }
    window.addEventListener('resize', crop);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(crop);
    if (cv) {
      home.querySelector('.splash').addEventListener('click', go);  // примерка: дольше обычного, 8 секунд
      setTimeout(go, 8000);
    } else {
      // Как у Levitt: обложка держится 3 с с момента открытия страницы, при каждом заходе.
      // Если фото к этому времени ещё не загрузилось, ждём его (но не дольше 9 с).
      var t0 = Date.now(), HOLD = 3000;
      var whenLoaded = function () { setTimeout(go, Math.max(0, HOLD - (Date.now() - t0))); };
      if (simg && !simg.complete) {
        simg.addEventListener('load', whenLoaded);
        simg.addEventListener('error', go);
        setTimeout(go, HOLD + 6000);
      } else {
        whenLoaded();
      }
    }

    var queued = false, wasPaused = null, wasTheme = null, lastP = -1;
    var splashTile = home.querySelector('.splash .tile');
    var vh = window.innerHeight, portrait = vh > window.innerWidth;
    var startY = 0;   // прокрутка, на которой текст показывается снизу
    function metrics() {
      // высоту берём один раз: на телефоне она «дышит» из-за адресной строки и даёт рывки
      vh = stage.clientHeight; portrait = vh > window.innerWidth;
      startY = content.offsetTop - vh;
    }
    metrics();
    function onScroll() {
      queued = false;
      // Пока заставка на экране, она не прилипает: уезжает вверх вместе со страницей
      if (!ready && splashTile) {
        splashTile.style.transform = 'translate3d(0,' + (-Math.min(window.pageYOffset, vh)).toFixed(1) + 'px,0)';
        if (window.pageYOffset > vh * .35) go();  // обложку увели прокруткой: дальше обычная главная
      }
      var p = (window.pageYOffset - startY) / (portrait ? vh / 2 : vh);
      p = p < 0 ? 0 : p > 1 ? 1 : p;
      var np = p > .01;
      if (np !== wasPaused) {
        wasPaused = paused = np;
        home.classList.toggle('is-content', np);
        if (!np) start();
      }
      // Как у Levitt: белый фон, пока плывут кадры; цвет пары, когда текст наехал на экран на 10%
      var th = p > .1;
      if (th !== wasTheme) { wasTheme = th; document.body.classList.toggle('is-theme', th); }
      if (p === lastP) return;
      lastP = p;
      if (portrait) {
        mark.style.transform = 'translate3d(' + (-50 * p).toFixed(2) + 'vw,0,0)';
        mark.style.opacity = (1 - p).toFixed(3);
        mark.style.visibility = p >= 1 ? 'hidden' : '';
      } else {
        mark.style.transform = 'translate3d(0,' + (-(vh - 20) * p).toFixed(1) + 'px,0)';
        mark.style.opacity = '';
        mark.style.visibility = '';
      }
    }
    function req() { if (!queued) { queued = true; requestAnimationFrame(onScroll); } }
    window.addEventListener('scroll', req, { passive: true });
    window.addEventListener('resize', function () { var w = W; measure(); if (W === w) return; items.forEach(function (it) { it.place(); }); draw(); metrics(); lastP = -1; req(); });
    onScroll();
  }

  // Лайтбокс
  var lb = document.querySelector('.lb');
  var cur = 0;
  function show(i) {
    cur = (i + links.length) % links.length;
    lb.querySelector('img').src = links[cur].href;
    lb.querySelector('.c').textContent = (cur + 1) + ' / ' + links.length;
    lb.classList.add('open');
  }
  function hide() { lb.classList.remove('open'); lb.querySelector('img').removeAttribute('src'); }
  links.forEach(function (a, i) {
    a.addEventListener('click', function (e) { e.preventDefault(); show(i); });
  });
  if (lb) {
    lb.querySelector('.x').addEventListener('click', hide);
    lb.querySelector('.p').addEventListener('click', function () { show(cur - 1); });
    lb.querySelector('.nx').addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) hide(); });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { if (lb && lb.classList.contains('open')) hide(); else setMenu(false); }
    if (lb && lb.classList.contains('open')) {
      if (e.key === 'ArrowLeft') show(cur - 1);
      if (e.key === 'ArrowRight') show(cur + 1);
    }
  });
})();
