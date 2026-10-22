from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width":360,"height":740}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    errs=[]
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///workspace/index.html"); pg.wait_for_timeout(500)

    # call bar exists & visible
    print("callbar visible:", pg.is_visible(".m-callbar"))
    # open drawer
    pg.tap(".burger"); pg.wait_for_timeout(700)
    box = pg.eval_on_selector(".nav-links", "e=>{const r=e.getBoundingClientRect();return {top:r.top,bottom:r.bottom,left:r.left,right:r.right}}")
    vis = pg.eval_on_selector(".burger span", "e=>getComputedStyle(e).backgroundColor")
    print("drawer box:", box, "burger color:", vis)
    print("scrim visible:", pg.is_visible(".nav-scrim"), "| body overflow:", pg.evaluate("document.body.style.overflow"))
    pg.screenshot(path=".audit/drawer-open.png")
    # tap scrim to close
    pg.mouse.click(180, 700); pg.wait_for_timeout(700)
    print("closed:", pg.evaluate("document.querySelector('.nav-links').classList.contains('open')"))
    # reopen and navigate
    pg.tap(".burger"); pg.wait_for_timeout(600)
    pg.tap(".nav-links a[href='reviews.html']"); pg.wait_for_timeout(900)
    print("navigated:", pg.url.endswith("reviews.html"), "| drawer closed after nav:", not pg.evaluate("document.querySelector('.nav-links').classList.contains('open')"))
    # filter rail works
    pg.tap(".filter-btn[data-filter='foot-pain']" if pg.query_selector(".filter-btn[data-filter='foot-pain']") else ".filters button:nth-child(2)")
    pg.wait_for_timeout(400)
    print("live count:", pg.text_content(".review-count-live"))
    pg.screenshot(path=".audit/reviews-mobile.png")
    # scroll page fully; check no horizontal pan
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(400)
    print("scrollWidth-ok:", pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth"))
    # contact page: map + hours
    pg.goto("file:///workspace/contact.html"); pg.wait_for_timeout(600)
    pg.screenshot(path=".audit/contact-mobile.png", full_page=False)
    # index hero shot
    pg.goto("file:///workspace/index.html"); pg.wait_for_timeout(800)
    pg.screenshot(path=".audit/home-mobile.png")
    print("JS errors:", errs or "none")
    ctx.close(); b.close()
