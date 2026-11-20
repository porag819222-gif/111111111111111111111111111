/* Taleora Studio — interactions
   Theme · language · nav · reveal/scroll (GSAP) · tilt · portfolio · dialogs · hero 3D (Three.js) */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var root = document.documentElement;
  var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = matchMedia("(hover:hover) and (pointer:fine)").matches;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var lang = function () { return root.lang === "bn" ? "bn" : "en"; };
  var L = function (pair) { return pair[lang() === "bn" ? 1 : 0]; };

  /* ---------- theme ---------- */
  var themeBtn = $("#theme");
  function syncTheme() {
    var dark = root.getAttribute("data-theme") === "dark";
    themeBtn.setAttribute("aria-pressed", dark);
    themeBtn.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
    var m = $('meta[name="theme-color"]'); if (m) m.content = dark ? "#141414" : "#FAF8F3";
  }
  themeBtn.addEventListener("click", function () {
    root.classList.add("theme-anim");
    var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next); store.set("taleora-theme", next); syncTheme();
    setTimeout(function () { root.classList.remove("theme-anim"); }, 600);
  });
  syncTheme();

  /* ---------- language ---------- */
  function setLang(l) {
    root.lang = l; store.set("taleora-lang", l);
    var b = $("#lang"); if (b) b.setAttribute("aria-label", l === "bn" ? "Switch to English" : "বাংলায় দেখুন");
    var pairs = [["#pl-idea", "আপনার আইডিয়া সংক্ষেপে লিখুন", "Briefly describe your idea"], ["#pl-name", "আপনার নাম", "Your name"]];
    pairs.forEach(function (p) { var e = $(p[0]); if (e) e.placeholder = l === "bn" ? p[1] : p[2]; });
    if (dlgOpenFn) dlgOpenFn();
  }
  var dlgOpenFn = null;
  $("#lang").addEventListener("click", function () { setLang(lang() === "bn" ? "en" : "bn"); });
  setLang(lang());

  /* ---------- nav ---------- */
  var nav = $("#nav"), burger = $("#burger"), mmenu = $("#mmenu"), toTop = $("#to-top");
  function onScroll() {
    nav.classList.toggle("solid", window.scrollY > 24);
    toTop.classList.toggle("show", window.scrollY > 900);
  }
  addEventListener("scroll", onScroll, { passive: true }); onScroll();
  function menu(open) {
    mmenu.classList.toggle("open", open); burger.setAttribute("aria-expanded", open);
    mmenu.setAttribute("aria-hidden", !open); document.body.style.overflow = open ? "hidden" : "";
    if (open) { var a = $("a", mmenu); a && setTimeout(function () { a.focus(); }, 80); }
  }
  burger.addEventListener("click", function () { menu(!mmenu.classList.contains("open")); });
  $$("a", mmenu).forEach(function (a) { a.addEventListener("click", function () { menu(false); }); });
  addEventListener("keydown", function (e) { if (e.key === "Escape" && mmenu.classList.contains("open")) { menu(false); burger.focus(); } });
  matchMedia("(min-width:1101px)").addEventListener("change", function (m) { if (m.matches) menu(false); });
  toTop.addEventListener("click", function () { scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" }); });
  // active link
  var links = {}; $$(".links a").forEach(function (a) { links[a.dataset.nav] = a; });
  var spy = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      var id = e.target.id; if (id === "preview-payment") id = "how"; if (id === "why") id = "about";
      Object.keys(links).forEach(function (k) { links[k].classList.toggle("on", k === id); links[k].toggleAttribute("aria-current", k === id); });
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  $$("main > section[id]").forEach(function (s) { spy.observe(s); });

  /* ---------- reveal / scroll motion ---------- */
  function initMotion() {
    var g = window.gsap, ST = window.ScrollTrigger;
    if (!g || !ST || reduced) { root.classList.add("reduced"); $$(".shimmer img").forEach(function () {}); return; }
    g.registerPlugin(ST);
    // hero entrance
    g.from("[data-hero]", { y: 36, opacity: 0, duration: 1.1, ease: "power3.out", stagger: .12, delay: .1, clearProps: "transform,opacity" });
    // reveals
    ST.batch("[data-rv]", {
      start: "top 88%", once: true,
      onEnter: function (els) { g.to(els, { opacity: 1, y: 0, duration: .9, ease: "power3.out", stagger: .09, overwrite: true }); }
    });
    // make sure positions are right after fonts/images/scroll-restoration, and never leave content hidden
    var refresh = function () { ST.refresh(); };
    addEventListener("load", function () { refresh(); setTimeout(refresh, 400); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(refresh);
    setTimeout(function () {
      $$("[data-rv]").forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < innerHeight && r.bottom > 0 && parseFloat(getComputedStyle(el).opacity) < .05) g.to(el, { opacity: 1, y: 0, duration: .6 });
      });
    }, 2200);
    // image parallax in banners / about
    $$("[data-parallax]").forEach(function (img) {
      g.fromTo(img, { yPercent: -7 }, { yPercent: 7, ease: "none", scrollTrigger: { trigger: img.parentNode, start: "top bottom", end: "bottom top", scrub: .6 } });
    });
    // hero art drifts
    var ha = $(".hero-art img");
    if (ha) g.to(ha, { yPercent: -6, ease: "none", scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true } });
    // journey progress lines
    $$("[data-journey]").forEach(function (j) {
      var fill = $(".fill", j), steps = $$(".step", j);
      if (!fill) return;
      var wide = matchMedia("(min-width:961px)");
      g.fromTo(fill, { width: 0 }, { width: "75%", ease: "none", scrollTrigger: { trigger: $(".steps", j), start: "top 75%", end: "bottom 55%", scrub: .5 } });
    });
  }

  /* ---------- 3D tilt on service cards ---------- */
  if (finePointer && !reduced) {
    $$("[data-tilt]").forEach(function (c) {
      var raf = 0;
      c.addEventListener("pointermove", function (e) {
        var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(function () {
          c.style.transform = "perspective(1000px) rotateY(" + ((x - .5) * 5) + "deg) rotateX(" + ((.5 - y) * 4) + "deg) translateY(-4px)";
          c.style.setProperty("--gx", x * 100 + "%"); c.style.setProperty("--gy", y * 100 + "%");
        });
      });
      c.addEventListener("pointerleave", function () { cancelAnimationFrame(raf); c.style.transform = ""; });
    });
  }

  /* ---------- dialogs ---------- */
  function openDlg(d) { if (typeof d.showModal === "function") d.showModal(); else d.setAttribute("open", ""); document.body.style.overflow = "hidden"; }
  function closeDlg(d) { if (d.open) d.close(); document.body.style.overflow = ""; }
  $$("dialog").forEach(function (d) {
    d.addEventListener("click", function (e) { if (e.target === d || (e.target.closest && e.target.closest("[data-close]"))) closeDlg(d); });
    d.addEventListener("close", function () {
      document.body.style.overflow = ""; dlgOpenFn = null;
      var v = $("video", d); if (v) { v.pause(); v.removeAttribute("src"); v.load(); }
      if (d._from) d._from.focus();
    });
  });

  var DATA = {}; try { DATA = JSON.parse($("#svc-data").textContent); } catch (e) {}
  var svcDlg = $("#svc-dlg");
  function fillSvc(id) {
    var s = DATA[id]; if (!s) return;
    $("#svc-title").textContent = L(s.name);
    $("#svc-kind").textContent = L(s.kind);
    $("#svc-desc").textContent = L(s.desc);
    $("#svc-img").src = s.img;
    $("#svc-price").innerHTML = '<div class="price"><span class="p-label">' + L(s.kind) + '</span><span class="p-val"><span class="cur">৳</span>' + s.price + "</span></div>";
    $("#svc-wl").textContent = L(s.whenLabel); $("#svc-w").textContent = L(s.when);
    $("#svc-items").innerHTML = s.items.map(function (i) { return "<li>" + L(i) + "</li>"; }).join("");
    $("#svc-suit").textContent = L(s.suit);
    var steps = lang() === "bn"
      ? ["নিচের বোতামে আমাদের অফিসিয়াল ফেসবুক পেজে যান।", "সার্ভিসের নাম ও আপনার আইডিয়া জানান।", s.video ? "আমরা কনসেপ্ট ও বিস্তারিত নিশ্চিত করে কাজ শুরু করি।" : "আমরা বিস্তারিত ও স্কোপ নিশ্চিত করে কাজ শুরু করি।"]
      : ["Use the button below to open our official Facebook page.", "Tell us the service name and your idea.", s.video ? "We confirm the concept and details, then begin." : "We confirm the details and scope, then begin."];
    $("#svc-order").innerHTML = steps.map(function (x) { return "<li>" + x + "</li>"; }).join("");
  }
  $$("[data-svc]").forEach(function (b) {
    b.addEventListener("click", function () {
      var id = b.dataset.svc; svcDlg._from = b; fillSvc(id); dlgOpenFn = function () { fillSvc(id); }; openDlg(svcDlg);
    });
  });

  /* ---------- portfolio ---------- */
  var pfDlg = $("#pf-dlg"), player = $("#pf-player");
  function openPf(el) {
    var v = el.dataset.kind === "video";
    var fill = function () {
      var bl = lang() === "bn";
      $("#pf-title").textContent = el.dataset.title;
      $("#pf-badge").textContent = bl ? el.dataset.badgeBn : el.dataset.badgeEn;
      var lab = bl ? el.dataset.labelBn : el.dataset.labelEn;
      $("#pf-sub").textContent = v ? lab : lab + " — " + (bl ? el.dataset.aboutBn : el.dataset.aboutEn);
    };
    fill(); dlgOpenFn = fill; pfDlg._from = el;
    $("#pf-video").hidden = !v; $("#pf-concept").hidden = v;
    $("#pf-box").classList.toggle("portrait", v && el.dataset.portrait === "1");
    if (v) { player.poster = el.dataset.poster; player.src = el.dataset.src; }
    else { $("#pf-img").src = el.dataset.img; $("#pf-img").alt = el.dataset.title + " — concept artwork"; }
    openDlg(pfDlg);
    if (v) { var p = player.play(); if (p && p.catch) p.catch(function () {}); }
  }
  $$(".pf").forEach(function (p) {
    p.addEventListener("click", function () { openPf(p); });
    var im = $("img", p);
    if (im) { var done = function () { p.classList.remove("shimmer"); }; if (im.complete) done(); else im.addEventListener("load", done); }
  });
  $$(".svc .media img").forEach(function (im) { if (im.complete) im.parentNode.classList.remove("shimmer"); });
  $$(".chip").forEach(function (c) {
    c.addEventListener("click", function () {
      var f = c.dataset.filter;
      $$(".chip").forEach(function (x) { x.setAttribute("aria-pressed", x === c); });
      $$(".pf").forEach(function (p) {
        var show = f === "all" || p.dataset.cat === f;
        p.classList.toggle("hide", !show);
        if (show) { p.classList.remove("reveal-in"); void p.offsetWidth; if (!reduced) p.classList.add("reveal-in"); }
      });
    });
  });

  /* ---------- video preview / payment illustration ---------- */
  var player2 = $("#player"), stamp = $("#stamp");
  $$(".toggle button").forEach(function (b) {
    b.addEventListener("click", function () {
      var paid = b.dataset.state === "paid";
      $$(".toggle button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      player2.classList.toggle("paid", paid);
      stamp.innerHTML = paid
        ? '<span class="en">Final video, watermark removed</span><span class="bn">ফাইনাল ভিডিও, ওয়াটারমার্ক ছাড়া</span>'
        : '<span class="en">Preview with watermark</span><span class="bn">ওয়াটারমার্কসহ প্রিভিউ</span>';
    });
  });

  /* ---------- message planner (copies text only; sends nothing) ---------- */
  var copyBtn = $("#pl-copy");
  if (copyBtn) copyBtn.addEventListener("click", function () {
    var v = function (id) { return ($("#" + id).value || "").trim(); };
    var msg = "Hello Taleora Studio!\n" +
      (v("pl-name") ? "Name: " + v("pl-name") + "\n" : "") +
      (v("pl-svc") ? "Service: " + v("pl-svc") + "\n" : "") +
      (v("pl-idea") ? "My idea: " + v("pl-idea") + "\n" : "") +
      (v("pl-date") ? "Needed by: " + v("pl-date") + "\n" : "");
    var ok = $("#pl-ok");
    function done() { ok.classList.add("show"); setTimeout(function () { ok.classList.remove("show"); }, 5000); }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(msg).then(done, done);
    else { var ta = document.createElement("textarea"); ta.value = msg; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); } catch (e) {} ta.remove(); done(); }
  });

  /* ---------- hero: pointer depth + Three.js light trails & dust ---------- */
  var hv = $("#hero-visual");
  if (hv && finePointer && !reduced) {
    var mems = $$(".mem", hv), art = $(".hero-art", hv), tx = 0, ty = 0, cx = 0, cy = 0;
    hv.addEventListener("pointermove", function (e) {
      var r = hv.getBoundingClientRect(); tx = (e.clientX - r.left) / r.width - .5; ty = (e.clientY - r.top) / r.height - .5;
    });
    hv.addEventListener("pointerleave", function () { tx = ty = 0; });
    (function tick() {
      cx += (tx - cx) * .08; cy += (ty - cy) * .08;
      mems.forEach(function (m) { var d = +m.dataset.depth || 20; m.style.setProperty("--px", (-cx * d) + "px"); m.style.setProperty("--py", (-cy * d) + "px"); });
      if (art) art.style.transform = "rotateY(" + (cx * 4) + "deg) rotateX(" + (-cy * 3) + "deg)";
      requestAnimationFrame(tick);
    })();
  }

  function initHero3D() {
    var cv = $("#hero-gl");
    if (!cv || reduced || !window.THREE) return;
    var mobile = innerWidth < 760;
    var weak = (navigator.hardwareConcurrency || 4) <= 2 || (navigator.deviceMemory || 4) <= 2;
    if (weak) return;
    var T = window.THREE, R;
    try { R = new T.WebGLRenderer({ canvas: cv, alpha: true, antialias: !mobile, powerPreference: "low-power" }); } catch (e) { return; }
    R.setPixelRatio(Math.min(devicePixelRatio || 1, mobile ? 1.25 : 2));
    var S = new T.Scene(), C = new T.PerspectiveCamera(40, 1, .1, 50); C.position.z = 10;

    // soft round sprite
    var c2 = document.createElement("canvas"); c2.width = c2.height = 64; var g = c2.getContext("2d");
    var gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, "rgba(255,244,214,1)"); gr.addColorStop(.35, "rgba(226,190,120,.85)"); gr.addColorStop(1, "rgba(214,183,125,0)");
    g.fillStyle = gr; g.fillRect(0, 0, 64, 64); var sprite = new T.CanvasTexture(c2);

    var N = mobile ? 70 : 170, pos = new Float32Array(N * 3), sp = [];
    for (var i = 0; i < N; i++) { pos[i * 3] = (Math.random() - .5) * 15; pos[i * 3 + 1] = (Math.random() - .5) * 9; pos[i * 3 + 2] = (Math.random() - .5) * 6; sp.push(.15 + Math.random() * .4); }
    var pg = new T.BufferGeometry(); pg.setAttribute("position", new T.BufferAttribute(pos, 3));
    var dust = new T.Points(pg, new T.PointsMaterial({ map: sprite, size: mobile ? .2 : .22, transparent: true, opacity: .95, depthWrite: false, sizeAttenuation: true }));
    S.add(dust);

    // light trails: thin tubes with fading alpha along their length
    var trails = [];
    function trail(pts, w, op) {
      var curve = new T.CatmullRomCurve3(pts.map(function (p) { return new T.Vector3(p[0], p[1], p[2]); }));
      var geo = new T.TubeGeometry(curve, 120, w, 6, false), cols = [], n = geo.attributes.position.count;
      var seg = 7; // radial segments + 1
      for (var k = 0; k < n; k++) { var t = Math.floor(k / seg) / 120; cols.push(1, .82 + t * .06, .5 + t * .2, Math.sin(t * Math.PI) * op); }
      geo.setAttribute("color", new T.BufferAttribute(new Float32Array(cols), 4));
      var m = new T.Mesh(geo, new T.MeshBasicMaterial({ vertexColors: true, transparent: true, depthWrite: false }));
      S.add(m); trails.push(m);
    }
    trail([[-7, -2.2, 0], [-3.5, -.2, 1], [0, -1.8, .4], [3.5, .8, 1.2], [7, -.4, 0]], .028, .85);
    if (!mobile) trail([[-6.5, 2.6, -1], [-2, 1.6, .5], [2.5, 2.9, 0], [6.5, 1.2, -.5]], .018, .6);

    function size() { var w = cv.clientWidth, h = cv.clientHeight; if (!w || !h) return; R.setSize(w, h, false); C.aspect = w / h; C.updateProjectionMatrix(); }
    size(); addEventListener("resize", size);
    var visible = true; new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(cv);
    var mx = 0, my = 0; addEventListener("pointermove", function (e) { mx = e.clientX / innerWidth - .5; my = e.clientY / innerHeight - .5; }, { passive: true });
    var t0 = performance.now();
    (function loop(now) {
      requestAnimationFrame(loop);
      if (!visible || document.hidden) return;
      var t = (now - t0) / 1000, p = pg.attributes.position.array;
      for (var i = 0; i < N; i++) { p[i * 3 + 1] += sp[i] * .004; p[i * 3] += Math.sin(t * .5 + i) * .0016; if (p[i * 3 + 1] > 4.6) p[i * 3 + 1] = -4.6; }
      pg.attributes.position.needsUpdate = true;
      trails.forEach(function (m, k) { m.rotation.z = Math.sin(t * .25 + k) * .04; m.position.y = Math.sin(t * .6 + k * 2) * .18; });
      C.position.x += (mx * .9 - C.position.x) * .04; C.position.y += (-my * .6 - C.position.y) * .04; C.lookAt(0, 0, 0);
      R.render(S, C);
    })(t0);
    cv.classList.add("on");
  }

  function boot() {
    initMotion();
    // start 3D once the hero art has painted, keeping first paint light
    var go = function () { try { initHero3D(); } catch (e) {} };
    if ("requestIdleCallback" in window) requestIdleCallback(go, { timeout: 1500 }); else setTimeout(go, 400);
  }
  var lazy3d = document.createElement("script");
  lazy3d.src = "assets/vendor/three.min.js"; lazy3d.async = true;
  function ready() { if (window.gsap && window.ScrollTrigger) { loadThree(); } else setTimeout(ready, 30); }
  function loadThree() { lazy3d.onload = boot; lazy3d.onerror = function () { initMotion(); }; if (reduced) { boot(); } else document.head.appendChild(lazy3d); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ready); else ready();
})();
