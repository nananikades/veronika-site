(function () {
  // Меню
  var menu = document.querySelector('.menu');
  var btn = document.querySelector('.menu-btn');
  function setMenu(open) {
    menu.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open);
    btn.textContent = open ? btn.dataset.close : btn.dataset.open;
    document.body.style.overflow = open ? 'hidden' : '';
  }
  btn.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });

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
    var items = els.map(function (el, i) {
      var img = el.querySelector('img');
      var it = { el: el, img: img, dur: i % 2 === 0 ? 30 : 40, p: (i / 8 + .2) % 1, top: 0 };
      var place = function () {
        var small = W < 800, add = W < 768 ? 12.5 : (W <= 992 ? 10 : 0);
        var land = +img.getAttribute('width') > +img.getAttribute('height');
        it.top = i % 2 === 0 ? (small ? rnd(-2.5, 20) : rnd(-5, 15)) : (small ? rnd(50, 75) : rnd(40, 60));
        el.style.width = ((land ? rnd(20, 30) : rnd(15, 20)) + add) + '%';
      };
      it.place = place;
      if (img.complete) place(); else { img.addEventListener('load', function () { place(); draw(); }); place(); }
      return it;
    });
    function draw() {
      var end = W < 800 ? -.4 : -.25;
      items.forEach(function (it) {
        var x = (1 + (end - 1) * it.p) * W;
        it.el.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + (it.top / 100 * H).toFixed(1) + 'px,0)';
      });
    }
    draw();
    // Цикл работает только пока кадры плывут: во время прокрутки страницы скрипт ничего не двигает
    var ready = false, paused = false, speed = 1, last = 0, raf = 0;
    function tick(now) {
      raf = 0;
      if (paused || !ready) return;
      var dt = Math.min(now - last, 100) / 1000; last = now;
      items.forEach(function (it) {
        it.p += dt * speed / it.dur;
        if (it.p >= 1) { it.p -= 1; it.place(); }
      });
      draw();
      raf = requestAnimationFrame(tick);
    }
    function start() { if (raf || reduce || paused || !ready) return; last = performance.now(); raf = requestAnimationFrame(tick); }
    els.forEach(function (el) {
      el.addEventListener('mouseenter', function () { speed = .5; });
      el.addEventListener('mouseleave', function () { speed = 1; });
    });
    var seen = false;
    try { seen = sessionStorage.getItem('splash') === '1'; sessionStorage.setItem('splash', '1'); } catch (err) {}
    var go = function () { home.classList.add('ready'); ready = true; start(); };
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
    window.addEventListener('resize', crop);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(crop);
    if (cv) {
      home.querySelector('.splash').addEventListener('click', go);  // примерка: дольше обычного, 8 секунд
      setTimeout(go, 8000);
    } else {
      setTimeout(go, seen ? 300 : 3000);
    }

    var queued = false, wasPaused = null, lastP = -1;
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
      if (p === lastP) return;
      lastP = p;
      if (portrait) {
        mark.style.transform = 'translate3d(' + (-50 * p).toFixed(2) + 'vw,0,0) rotate(180deg)';
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
  var links = Array.prototype.slice.call(document.querySelectorAll('a[data-lb]'));
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
