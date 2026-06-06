import webview, asyncio, threading, sys, os, json
from pathlib import Path
sys.path.append(os.path.dirname(__file__))
from crownstar_core import CrownStarCognitive

TIER = "Pro"
MAX_INPUT = 2000000
MAX_OUTPUT = 500000000
MAX_FILE_BYTES = 2147483648
AMENITIES = [Picture','Video','CAD]

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
    def export_conversation(self, data):
        try:
            with open("crownstar_export.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return "Exported to crownstar_export.json"
        except Exception as e:
            return f"Export failed: {str(e)}"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    template_path = resource_path("index.template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("Pro", TIER)
    html = html.replace("2000000", str(MAX_INPUT))
    html = html.replace("500000000", str(MAX_OUTPUT))
    html = html.replace("2147483648", str(MAX_FILE_BYTES))
    html = html.replace("[Picture','Video','CAD]", json.dumps(AMENITIES))
    webview.create_window(f"CrownStar {TIER}", html=html, js_api=API())
    webview.start()

if __name__ == "__main__":
    main()

