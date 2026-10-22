from playwright.sync_api import sync_playwright
import json

PAGES = ["index.html","services.html","reviews.html","contact.html"]
VIEWPORTS = [(360,740),(390,844),(768,1024)]

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    for w,h in VIEWPORTS:
        ctx = b.new_context(viewport={"width":w,"height":h}, device_scale_factor=2)
        pg = ctx.new_page()
        errs=[]
        pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        for name in PAGES:
            pg.goto(f"file:///workspace/{name}")
            pg.wait_for_timeout(600)
            res = pg.evaluate("""() => {
              const out = {overflowX: document.documentElement.scrollWidth - window.innerWidth, offenders: [], smallTargets: [], tapTooClose: []};
              const vw = window.innerWidth;
              document.querySelectorAll('body *').forEach(el=>{
                const r = el.getBoundingClientRect();
                if(r.width===0&&r.height===0) return;
                if(r.right > vw+1 || r.left < -1){
                  if(getComputedStyle(el).position==='fixed') return;
                  out.offenders.push(el.tagName+'.'+(el.className.baseVal!==undefined?el.className.baseVal:el.className).toString().split(' ').slice(0,2).join('.')+' L'+Math.round(r.left)+' R'+Math.round(r.right));
                }
              });
              document.querySelectorAll('a,button,summary,input,.filter-btn').forEach(el=>{
                const r = el.getBoundingClientRect();
                if(r.width===0) return;
                if(Math.min(r.width,r.height) < 40) out.smallTargets.push((el.tagName+':'+(el.textContent||'').trim().slice(0,25))+' h='+Math.round(r.height)+' w='+Math.round(r.width));
              });
              out.offenders=[...new Set(out.offenders)].slice(0,12);
              out.smallTargets=[...new Set(out.smallTargets)].slice(0,15);
              return out;
            }""")
            print(f"\n=== {w}x{h} {name} ===")
            print(json.dumps(res, indent=1))
            if errs: print("JS ERRORS:", errs)
        ctx.close()
    b.close()
