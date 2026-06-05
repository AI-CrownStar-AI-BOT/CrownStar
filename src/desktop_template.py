import webview, asyncio, threading, sys, os, json
sys.path.append(os.path.dirname(__file__))
from crownstar_core import CrownStarCognitive

TIER = "{{TIER}}"
LIMITS = {{LIMITS}}
AMENITIES = {{AMENITIES}}
engine = CrownStarCognitive(tier=TIER)

class API:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self._run_loop, daemon=True).start()
    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    def chat(self, query):
        try:
            future = asyncio.run_coroutine_threadsafe(engine.think(query), self.loop)
            return future.result(timeout=30)
        except Exception as e:
            return f"⚠️ Core error: {str(e)}"

html = """
<!DOCTYPE html>
<html>
<head><title>CrownStar {{TIER}}</title></head>
<body style="background:#0a0c1a;color:#fff;font-family:sans-serif;">
<h1>⭐ CrownStar {{TIER}}</h1>
<input id="q" type="text" placeholder="Ask anything..." style="width:80%;padding:8px;">
<button onclick="send()">Send</button>
<div id="out" style="margin-top:20px;white-space:pre-wrap;"></div>
<script>
function send() {
    var q = document.getElementById('q').value;
    document.getElementById('out').innerText = "Thinking...";
    window.pywebview.api.chat(q).then(function(a) {
        document.getElementById('out').innerText = a;
    });
}
</script>
</body>
</html>
"""

def main():
    webview.create_window(f"CrownStar {TIER}", html=html, js_api=API())
    webview.start()
if __name__ == "__main__":
    main()
