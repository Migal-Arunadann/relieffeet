/* ==========================================================================
   RELIEF FEET — vanilla JS enhancements (progressive, no dependencies)
   ========================================================================== */
(function () {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------------
     1. Header scroll state
  --------------------------------------------------------------- */
  const header = document.querySelector(".site-header");
  if (header) {
    const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------------------------------------------------------
     2. Mobile burger menu
  --------------------------------------------------------------- */
  const burger = document.querySelector(".burger");
  const navLinks = document.querySelector(".nav-links");
  if (burger && navLinks) {
    burger.addEventListener("click", () => {
      const open = burger.getAttribute("aria-expanded") === "true";
      burger.setAttribute("aria-expanded", String(!open));
      navLinks.classList.toggle("open", !open);
      document.body.style.overflow = !open ? "hidden" : "";
    });
    navLinks.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        burger.setAttribute("aria-expanded", "false");
        navLinks.classList.remove("open");
        document.body.style.overflow = "";
      })
    );
  }

  /* ---------------------------------------------------------------
     3. Split headline text into words + letters for the
        staggered drop-in animation ("decode" effect).
        Runs on elements marked [data-decode].
  --------------------------------------------------------------- */
  function splitLetters(el) {
    const raw = el.textContent;
    el.removeAttribute("data-decode");
    el.setAttribute("aria-label", raw);
    let i = 0;
    const frag = document.createDocumentFragment();
    raw.split(/(\s+)/).forEach((token) => {
      if (/^\s+$/.test(token)) {
        frag.appendChild(document.createTextNode(" "));
        return;
      }
      const word = document.createElement("span");
      word.className = "word";
      token.split("").forEach((c) => {
        const ch = document.createElement("span");
        ch.className = "ch";
        ch.textContent = c;
        ch.style.setProperty("--i", i++);
        ch.setAttribute("aria-hidden", "true");
        word.appendChild(ch);
      });
      frag.appendChild(word);
    });
    el.textContent = "";
    el.appendChild(frag);
    el.classList.add("decode");
  }
  document.querySelectorAll("[data-decode]").forEach((el) => {
    if (!reduceMotion) splitLetters(el);
  });

  /* ---------------------------------------------------------------
     4. Reveal-on-scroll via IntersectionObserver
  --------------------------------------------------------------- */
  const revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      revealEls.forEach((el) => el.classList.add("in"));
    } else {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((e) => {
            if (e.isIntersecting) {
              e.target.classList.add("in");
              io.unobserve(e.target);
            }
          });
        },
        { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
      );
      revealEls.forEach((el) => io.observe(el));
    }
  }

  /* ---------------------------------------------------------------
     5. Count-up numbers (stats strip)
  --------------------------------------------------------------- */
  const counters = document.querySelectorAll("[data-count]");
  if (counters.length) {
    const run = (el) => {
      const target = parseFloat(el.dataset.count);
      const suffix = el.dataset.suffix || "";
      const dur = 1400;
      const t0 = performance.now();
      const step = (t) => {
        const p = Math.min((t - t0) / dur, 1);
        const eased = 1 - Math.pow(1 - p, 4);
        el.textContent = Math.round(target * eased) + suffix;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    if (reduceMotion || !("IntersectionObserver" in window)) {
      counters.forEach((el) => {
        el.textContent = el.dataset.count + (el.dataset.suffix || "");
      });
    } else {
      const io2 = new IntersectionObserver(
        (entries) => {
          entries.forEach((e) => {
            if (e.isIntersecting) {
              run(e.target);
              io2.unobserve(e.target);
            }
          });
        },
        { threshold: 0.6 }
      );
      counters.forEach((el) => io2.observe(el));
    }
  }

  /* ---------------------------------------------------------------
     6. Magnetic buttons — subtle pull toward cursor (desktop only)
  --------------------------------------------------------------- */
  if (!reduceMotion && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    document.querySelectorAll(".btn, .tile").forEach((el) => {
      el.addEventListener("mousemove", (ev) => {
        const r = el.getBoundingClientRect();
        const x = (ev.clientX - r.left - r.width / 2) * 0.12;
        const y = (ev.clientY - r.top - r.height / 2) * 0.12;
        el.style.translate = `${x}px ${y}px`;
      });
      el.addEventListener("mouseleave", () => {
        el.style.translate = "0px 0px";
        el.style.transition = "translate 0.4s cubic-bezier(0.22,1,0.36,1)";
        setTimeout(() => (el.style.transition = ""), 400);
      });
    });
  }

  /* ---------------------------------------------------------------
     7. Hero parallax on pointer move (very subtle)
  --------------------------------------------------------------- */
  const heroFig = document.querySelector(".hero-figure");
  if (heroFig && !reduceMotion && window.matchMedia("(hover: hover)").matches) {
    const hero = heroFig.closest(".hero") || heroFig.parentElement;
    hero.addEventListener("mousemove", (ev) => {
      const r = hero.getBoundingClientRect();
      const nx = (ev.clientX - r.left) / r.width - 0.5;
      const ny = (ev.clientY - r.top) / r.height - 0.5;
      heroFig.style.transform = `translate(${nx * -14}px, ${ny * -10}px)`;
      heroFig.querySelectorAll(".badge-float").forEach((b, idx) => {
        b.style.transform = `translate(${nx * (22 + idx * 8)}px, ${ny * (16 + idx * 6)}px)`;
      });
    });
  }

  /* ---------------------------------------------------------------
     8. Reviews page — tag filtering (no forms involved)
  --------------------------------------------------------------- */
  const filterBtns = document.querySelectorAll(".filter-btn");
  const reviewCards = document.querySelectorAll("[data-tags]");
  const liveCount = document.querySelector(".review-count-live");
  if (filterBtns.length && reviewCards.length) {
    let active = "all";
    const apply = () => {
      let shown = 0;
      reviewCards.forEach((card) => {
        const tags = card.dataset.tags.split(",");
        const ok = active === "all" || tags.includes(active);
        card.hidden = !ok;
        if (ok) {
          shown++;
          // re-trigger pop-in animation
          if (!reduceMotion) {
            card.style.animation = "none";
            void card.offsetWidth; // reflow
            card.style.animation = "ch-pop 0.5s cubic-bezier(0.22,1.4,0.36,1) both";
          }
        }
      });
      if (liveCount) {
        liveCount.textContent =
          shown === reviewCards.length
            ? `Showing all ${shown} featured reviews`
            : `Showing ${shown} of ${reviewCards.length} featured reviews`;
      }
    };
    filterBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        filterBtns.forEach((b) => b.setAttribute("aria-pressed", "false"));
        btn.setAttribute("aria-pressed", "true");
        active = btn.dataset.filter;
        apply();
      });
    });
    // inject keyframes once
    const style = document.createElement("style");
    style.textContent =
      "@keyframes ch-pop{from{opacity:0;transform:scale(.94) translateY(10px)}to{opacity:1;transform:none}}";
    document.head.appendChild(style);
    apply();
  }

  /* ---------------------------------------------------------------
     9. Contact page — highlight today's row & local time
  --------------------------------------------------------------- */
  const dayRows = document.querySelectorAll("[data-day]");
  if (dayRows.length) {
    const today = new Date().toLocaleDateString("en-US", { weekday: "long" });
    dayRows.forEach((row) => {
      if (row.dataset.day === today) row.classList.add("today");
    });
  }
  const clockEl = document.getElementById("local-time");
  if (clockEl) {
    const tick = () => {
      // Chennai = UTC+5:30
      const now = new Date();
      const ist = new Date(now.getTime() + (now.getTimezoneOffset() + 330) * 60000);
      clockEl.textContent = ist.toLocaleTimeString("en-IN", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      });
    };
    tick();
    setInterval(tick, 1000);
  }

  /* ---------------------------------------------------------------
     10. Footer year
  --------------------------------------------------------------- */
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = new Date().getFullYear();
  });
})();
