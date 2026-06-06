import webview, asyncio, threading, sys, os, json
from pathlib import Path
sys.path.append(os.path.dirname(__file__))
TIER = "Enterprise"
MAX_INPUT = 5000000
MAX_OUTPUT = 1000000000
MAX_FILE_MB = 5120
USE_LLM = True

if USE_LLM:
    from llm_wrapper import CrownStarLLM
    engine = CrownStarLLM()
else:
    from crownstar_core import CrownStarCognitive
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
            future = asyncio.run_coroutine_threadsafe(self._async_chat(query), self.loop)
            return future.result(timeout=60)
        except Exception as e:
            return f"Error: {e}"
    async def _async_chat(self, query):
        if USE_LLM:
            return engine.think(query)
        else:
            return await engine.think(query)
    def update_settings(self, settings):
        if USE_LLM:
            return engine.update_settings(**settings)
        return "Free tier has no settings"
    def export_conversation(self, data):
        with open("crownstar_export.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return "Exported"

def resource_path(rel):
    try:
        base = sys._MEIPASS
    except:
        base = os.path.abspath(".")
    return os.path.join(base, rel)

def main():
    html_path = resource_path("index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    webview.create_window(f"CrownStar {TIER}", html=html, js_api=API())
    webview.start()

if __name__ == "__main__":
    main()

