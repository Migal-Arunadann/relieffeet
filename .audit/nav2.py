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
        # burger visible & tappable?
        burger = pg.query_selector(".burger")
        burger.tap()
        pg.wait_for_timeout(700)
        state = pg.evaluate("""() => {
          const nl = document.querySelector('.nav-links');
          const r = nl.getBoundingClientRect();
          const cs = getComputedStyle(nl);
          const b = document.querySelector('.burger').getBoundingClientRect();
          const topEl = document.elementFromPoint(b.left+b.width/2, b.top+b.height/2);
          return {open: nl.classList.contains('open'), vis: cs.visibility, top: Math.round(r.top), height: Math.round(r.height),
                  expanded: document.querySelector('.burger').getAttribute('aria-expanded'),
                  burgerClickable: !!(topEl && (topEl.closest('.burger'))),
                  bodyLocked: getComputedStyle(document.body).overflow};
        }""")
        print(name, "OPEN:", json.dumps(state))
        if name=="index.html":
            pg.screenshot(path=".audit/m-drawer.png")
        # tap a link -> should navigate or close
        # test scrim closes: tap at y=800? drawer covers full height; instead press Escape
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)
        closed = pg.evaluate("""() => ({open: document.querySelector('.nav-links').classList.contains('open'),
            vis: getComputedStyle(document.querySelector('.nav-links')).visibility,
            inert: document.querySelector('.nav-links').inert,
            bodyOverflow: getComputedStyle(document.body).overflow})""")
        print(name, "CLOSED:", json.dumps(closed))
        # reopen then tap burger again to close
        pg.tap(".burger"); pg.wait_for_timeout(650)
        pg.tap(".burger"); pg.wait_for_timeout(650)
        st2 = pg.evaluate("() => getComputedStyle(document.querySelector('.nav-links')).visibility")
        print(name, "REOPEN+CLOSE visibility:", st2)
        # overflow check
        ovf = pg.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        print(name, "overflowX:", ovf)
    # nav via drawer link click
    pg.goto("file:///workspace/index.html"); pg.wait_for_timeout(400)
    pg.tap(".burger"); pg.wait_for_timeout(700)
    pg.screenshot(path=".audit/m-drawer-index.png")
    pg.locator(".nav-links a", has_text="Services").tap()
    pg.wait_for_timeout(900)
    print("navigated to:", pg.url)
    if errs: print("JS ERRORS:", errs)
    b.close()
