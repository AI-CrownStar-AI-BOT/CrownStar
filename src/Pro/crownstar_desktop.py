import webview, asyncio, sys, os
sys.path.append(os.path.dirname(__file__))
from crownstar_core import CrownStarCognitive

TIER = "Pro"
MAX_INPUT = 2000000
MAX_OUTPUT = 500000000
AMENITIES = ['picture','video','cad']

engine = CrownStarCognitive(tier=TIER)

class API:
    def chat(self, query):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(engine.think(query))
            loop.close()
            if len(result) > MAX_OUTPUT: result = result[:MAX_OUTPUT] + "..."
            return result
        except Exception as e:
            return f"⚠️ Core error: {str(e)}"

html = f"""
<!DOCTYPE html>
<html>
<head><title>CrownStar {TIER}</title></head>
<body style="background:#0a0c1a;color:#eef4ff;font-family:sans-serif;padding:20px;">
<h1>⭐ CrownStar {TIER}</h1>
<input id="q" type="text" placeholder="Ask anything..." style="width:70%;padding:8px;">
<button onclick="ask()">Ask</button>
<div id="out" style="margin-top:20px;background:#1e293b;padding:10px;border-radius:8px;"></div>
<script>
async function ask() {{
    const q = document.getElementById('q').value.trim();
    if(!q) return;
    document.getElementById('out').innerText = "Thinking...";
    try {{
        const ans = await window.pywebview.api.chat(q);
        document.getElementById('out').innerText = ans;
    }} catch(e) {{
        document.getElementById('out').innerText = "Error: " + e.message;
    }}
}}
</script>
</body>
</html>
"""

def main():
    webview.create_window(f"CrownStar {TIER}", html=html, js_api=API())
    webview.start()

if __name__ == "__main__":
    main()
