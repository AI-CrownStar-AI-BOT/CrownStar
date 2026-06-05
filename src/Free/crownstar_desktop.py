import webview
import asyncio
import threading
import sys
import os

sys.path.append(os.path.dirname(__file__))
from crownstar_core import CrownStarCognitive

TIER = "Free"
MAX_INPUT = 500000
MAX_OUTPUT = 100000000

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
<head>
    <meta charset="UTF-8">
    <title>CrownStar Free</title>
    <style>
        body { background: #0a0c1a; color: #eef4ff; font-family: sans-serif; padding: 20px; }
        .chat-area { margin-top: 20px; }
        input, button { padding: 8px; margin: 5px; }
        #output { background: #1e293b; padding: 10px; border-radius: 8px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>⭐ CrownStar Free</h1>
    <div class="chat-area">
        <input id="query" type="text" placeholder="Ask anything...">
        <button id="ask">Ask</button>
        <div id="output"></div>
    </div>
    <script>
        const askBtn = document.getElementById('ask');
        const queryInput = document.getElementById('query');
        const outputDiv = document.getElementById('output');
        askBtn.onclick = async () => {
            const q = queryInput.value.trim();
            if (!q) return;
            outputDiv.innerText = "Thinking...";
            try {
                const answer = await window.pywebview.api.chat(q);
                outputDiv.innerText = answer;
            } catch(e) {
                outputDiv.innerText = "Error: " + e.message;
            }
        };
        queryInput.onkeypress = (e) => { if (e.key === 'Enter') askBtn.click(); };
    </script>
</body>
</html>
"""

def main():
    webview.create_window("CrownStar Free", html=html, js_api=API())
    webview.start()

if __name__ == "__main__":
    main()
