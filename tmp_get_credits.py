import os
from playwright.sync_api import sync_playwright

def get_credits():
    with sync_playwright() as pw:
        auth_file = "auth_refon45974_indevgo_com.json"
        ctx_kwargs = {"no_viewport": True, "viewport": {"width": 1920, "height": 1080}}
        if os.path.exists(auth_file):
            ctx_kwargs["storage_state"] = auth_file
        
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(**ctx_kwargs)
        page = context.new_page()
        page.goto("https://magiclight.ai/kids-story/")
        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except:
            pass
        
        # wait a bit more just in case
        page.wait_for_timeout(3000)
        
        data = page.evaluate("""() => {
            let res = [];
            // To get unique texts
            let seen = new Set();
            document.querySelectorAll('div, span, p, a, button').forEach(el => {
                let rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.top < 150) { 
                    // To check text nodes directly, avoiding parent elements capturing all text
                    let ownText = Array.from(el.childNodes)
                        .filter(n => n.nodeType === 3)
                        .map(n => n.textContent.trim())
                        .join('');
                    if (ownText && ownText.length > 0 && ownText.length < 20 && /[0-9]/.test(ownText)) {
                        if (!seen.has(ownText)) {
                            res.push({text: ownText, class: el.className});
                            seen.add(ownText);
                        }
                    }
                }
            });
            return res;
        }""")
        for item in data:
            print(f"Text: '{item['text']}', Class: '{item['class']}'")
            
        print("Done.")
        browser.close()

if __name__ == "__main__":
    get_credits()
