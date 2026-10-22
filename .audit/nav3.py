from playwright.sync_api import sync_playwright
import json

PAGES = ["index.html","services.html","reviews.html","contact.html"]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width":390,"height":844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    errs=[]
    pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
    for name in PAGES:
        pg.goto(f"file:///workspace/{name}")
        pg.wait_for_timeout(500)
        info = pg.evaluate("""() => {
          const bg = document.querySelector('.burger');
          const cs = getComputedStyle(bg);
          const r = bg.getBoundingClientRect();
          const topEl = document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
          return {display: cs.display, vis: cs.visibility, op: cs.opacity, rect: [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
                  topEl: topEl ? topEl.tagName+'.'+(topEl.className||'') : null};
        }""")
        print(name, "BURGER:", json.dumps(info))
        # force tap via JS click to bypass visibility check
        pg.evaluate("document.querySelector('.burger').click()")
        pg.wait_for_timeout(700)
        state = pg.evaluate("""() => {
          const nl = document.querySelector('.nav-links');
          const r = nl.getBoundingClientRect();
          const cs = getComputedStyle(nl);
          const b = document.querySelector('.burger').getBoundingClientRect();
          const topEl = document.elementFromPoint(b.left+b.width/2, b.top+b.height/2);
          return {open: nl.classList.contains('open'), vis: cs.visibility, z: cs.zIndex, top: Math.round(r.top), h: Math.round(r.height),
                  expanded: document.querySelector('.burger').getAttribute('aria-expanded'),
                  burgerTopEl: topEl ? topEl.tagName+'.'+(topEl.className||'') : null,
                  bodyLock: getComputedStyle(document.body).overflow};
        }""")
        print(name, "OPEN:", json.dumps(state))
        if name == "index.html": pg.screenshot(path=".audit/m-drawer.png")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(650)
        closed = pg.evaluate("() => ({vis: getComputedStyle(document.querySelector('.nav-links')).visibility, inert: document.querySelector('.nav-links').inert, bodyOverflow: getComputedStyle(document.body).overflow})")
        print(name, "CLOSED:", json.dumps(closed))
        ovf = pg.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        print(name, "overflowX:", ovf)
    # link navigation from drawer
    pg.goto("file:///workspace/index.html"); pg.wait_for_timeout(400)
    pg.evaluate("document.querySelector('.burger').click()"); pg.wait_for_timeout(700)
    pg.screenshot(path=".audit/m-drawer-index.png")
    pg.locator(".nav-links a", has_text="Services").first.click(force=True)
    pg.wait_for_timeout(1000)
    print("navigated to:", pg.url.split('/')[-1])
    if errs: print("JS ERRORS:", errs)
    b.close()
