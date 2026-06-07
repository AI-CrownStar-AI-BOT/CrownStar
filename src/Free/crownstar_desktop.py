import webview, asyncio, threading, sys, os, json, random
from pathlib import Path
sys.path.append(os.path.dirname(__file__))
from crownstar_core import CrownStarCognitive

TIER = "Free"
MAX_INPUT = 500000
MAX_OUTPUT = 100000000
MAX_FILE_MB = 500
ALLOWED_ADDONS = 25   # number of addon categories allowed for this tier

engine = CrownStarCognitive(tier=TIER)

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
        msgs = engine.memory.get_messages(int(conv_id))
        return [{"role":r, "content":c} for r,c in msgs]
    def store_message(self, conv_id, role, content):
        engine.memory.store_message(int(conv_id), role, content)
        return "ok"
    def get_files(self, conv_id):
        files = engine.memory.get_files(int(conv_id))
        return [{"filename":f, "content":c[:500]} for f,c in files]
    def store_file(self, conv_id, filename, content):
        engine.memory.store_file(int(conv_id), filename, content[:10000])
        return "ok"
    def get_addons(self):
        with open("addons.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    def save_addon(self, category, new_link):
        with open("addons.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if category in data:
            data[category]["links"].append(new_link)
            with open("addons.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        return "ok"
    def delete_addon(self, category, link):
        with open("addons.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if category in data and link in data[category]["links"]:
            data[category]["links"].remove(link)
            with open("addons.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        return "ok"
    def set_setting(self, key, value):
        engine.memory.set_setting(key, value)
        if key == "min_response_len":
            engine.min_response_len = int(value)
        return "ok"
    def get_setting(self, key):
        return engine.memory.get_setting(key)

def resource_path(rel):
    try: base = sys._MEIPASS
    except: base = os.path.abspath(".")
    return os.path.join(base, rel)

def main():
    html_path = resource_path("index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    webview.create_window(f"CrownStar {TIER}", html=html, js_api=API(), width=1400, height=900, min_size=(1000,700))
    webview.start()

if __name__ == "__main__":
    main()

