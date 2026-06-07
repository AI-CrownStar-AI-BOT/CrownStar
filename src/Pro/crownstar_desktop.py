import webview, asyncio, threading, sys, os, json
from pathlib import Path
sys.path.append(os.path.dirname(__file__))
from crownstar_core import CrownStarCognitive

TIER = "Pro"
MAX_INPUT = 2000000
MAX_OUTPUT = 500000000
MAX_FILE_MB = 2048
ALLOWED_ADDONS = 45

engine = CrownStarCognitive(tier=TIER)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

addons_path = resource_path("addons.json")
with open(addons_path, "r", encoding="utf-8") as f:
    ADDONS_DATA = json.load(f)

class API:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self._run_loop, daemon=True).start()
    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    def chat(self, query, conv_id, min_len):
        try:
            future = asyncio.run_coroutine_threadsafe(engine.think(query, int(conv_id), int(min_len)), self.loop)
            return future.result(timeout=30)
        except Exception as e:
            return f"Error: {e}"
    def get_messages(self, conv_id):
        return [{"role":r, "content":c} for r,c in engine.memory.get_messages(int(conv_id))]
    def store_message(self, conv_id, role, content):
        engine.memory.store_message(int(conv_id), role, content)
        return "ok"
    def get_files(self, conv_id):
        return [{"filename":f, "content":c[:500]} for f,c in engine.memory.get_files(int(conv_id))]
    def store_file(self, conv_id, filename, content):
        engine.memory.store_file(int(conv_id), filename, content[:10000])
        return "ok"
    def get_addons(self):
        return ADDONS_DATA
    def save_addon(self, category, new_link):
        if category in ADDONS_DATA:
            ADDONS_DATA[category]["links"].append(new_link)
            with open(addons_path, "w", encoding="utf-8") as f:
                json.dump(ADDONS_DATA, f, indent=2)
        return "ok"
    def delete_addon(self, category, link):
        if category in ADDONS_DATA and link in ADDONS_DATA[category]["links"]:
            ADDONS_DATA[category]["links"].remove(link)
            with open(addons_path, "w", encoding="utf-8") as f:
                json.dump(ADDONS_DATA, f, indent=2)
        return "ok"
    def set_setting(self, key, value):
        engine.memory.set_setting(key, value)
        if key == "min_response_len":
            engine.min_response_len = int(value)
        return "ok"
    def get_setting(self, key):
        return engine.memory.get_setting(key)

def main():
    html_path = resource_path("index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    webview.create_window(f"CrownStar {TIER}", html=html, js_api=API(), width=1400, height=900, min_size=(1000,700))
    webview.start()

if __name__ == "__main__":
    main()

