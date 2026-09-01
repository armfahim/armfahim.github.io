/* ============================================================
   A.R.M. Fahim — Portfolio interactions
   ============================================================ */
(function () {
  'use strict';

  /* ---- Theme toggle (persisted) ---- */
  var root = document.documentElement;
  var toggle = document.getElementById('themeToggle');
  var saved = null;
  try { saved = localStorage.getItem('theme'); } catch (e) {}
  if (saved) { root.setAttribute('data-theme', saved); }

  toggle.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  /* ---- Nav: shadow on scroll + scroll progress ---- */
  var nav = document.getElementById('nav');
  var progress = document.getElementById('scrollProgress');
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    nav.classList.toggle('scrolled', y > 10);
    var h = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- Mobile menu ---- */
  var burger = document.getElementById('navBurger');
  var links = document.getElementById('navLinks');
  burger.addEventListener('click', function () {
    burger.classList.toggle('open');
    links.classList.toggle('open');
  });
  links.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () {
      burger.classList.remove('open');
      links.classList.remove('open');
    });
  });

  /* ---- Active nav link on scroll ---- */
  var sections = document.querySelectorAll('section[id]');
  var navMap = {};
  document.querySelectorAll('.nav__links a').forEach(function (a) {
    navMap[a.getAttribute('href').slice(1)] = a;
  });
  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        document.querySelectorAll('.nav__links a').forEach(function (a) { a.classList.remove('active'); });
        var link = navMap[en.target.id];
        if (link) link.classList.add('active');
      }
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  sections.forEach(function (s) { spy.observe(s); });

  /* ---- Reveal on scroll ---- */
  var revealer = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        en.target.classList.add('visible');
        revealer.unobserve(en.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(function (el, i) {
    el.style.transitionDelay = (i % 4) * 0.08 + 's';
    revealer.observe(el);
  });

  /* ---- Count-up stats ---- */
  var counted = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target;
      var target = parseInt(el.getAttribute('data-count'), 10);
      var start = 0, dur = 1400, t0 = null;
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / dur, 1);
        el.textContent = Math.floor(p * (target - start) + start);
        if (p < 1) requestAnimationFrame(step);
        else el.textContent = target;
      }
      requestAnimationFrame(step);
      counted.unobserve(el);
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.stat__num').forEach(function (el) { counted.observe(el); });

  /* ---- Typewriter in hero ---- */
  var tw = document.getElementById('typewriter');
  if (tw) {
    var words = ['Java Developer', 'Spring Boot Expert', 'API Architect', 'Backend Engineer', 'Problem Solver'];
    var wi = 0, ci = 0, deleting = false;
    function tick() {
      var word = words[wi];
      tw.textContent = word.slice(0, ci);
      if (!deleting && ci < word.length) { ci++; setTimeout(tick, 90); }
      else if (!deleting && ci === word.length) { deleting = true; setTimeout(tick, 1600); }
      else if (deleting && ci > 0) { ci--; setTimeout(tick, 45); }
      else { deleting = false; wi = (wi + 1) % words.length; setTimeout(tick, 300); }
    }
    tick();
  }

  /* ---- Footer year ---- */
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
