# crownstar_desktop.py – Ultimate Desktop UI
import webview, asyncio, threading, sys, os, json, hashlib, base64
from pathlib import Path
sys.path.append(os.path.dirname(__file__))
from crownstar_core import CrownStarCognitive

TIER = "{{TIER}}"
MAX_INPUT = {{MAX_INPUT}}
MAX_OUTPUT = {{MAX_OUTPUT}}
MAX_FILE_MB = {{MAX_FILE_MB}}
ALLOWED_ADDONS = {{ALLOWED_ADDONS}}

engine = CrownStarCognitive(tier=TIER)

def resource_path(rel):
    try: base = sys._MEIPASS
    except: base = os.path.abspath(".")
    return os.path.join(base, rel)

# Load addons from GitHub topics (dynamic)
async def fetch_github_addons():
    async with aiohttp.ClientSession() as session:
        url = "https://api.github.com/search/topics?q=ai+game+tool+library+bot"
        async with session.get(url, headers={"Accept": "application/vnd.github.mercy-preview+json"}) as resp:
            if resp.status == 200:
                data = await resp.json()
                topics = data.get("items", [])[:ALLOWED_ADDONS]
                addons = {}
                for t in topics:
                    name = t["name"].capitalize()
                    addons[name] = {"icon": "🔧", "links": [t["url"]]}
                return addons
    return {}

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
            return future.result(timeout=45)
        except Exception as e:
            return f"Error: {e}"
    def get_messages(self, conv_id):
        return engine.memory.get_messages(int(conv_id))
    def get_conversations(self):
        return engine.memory.get_conversations()
    def new_conversation(self, title):
        return engine.memory.create_conversation(title)
    def search_messages(self, query):
        return engine.memory.search_messages(query, 20)
    def store_message(self, conv_id, role, content):
        engine.memory.store_message(int(conv_id), role, content)
        return "ok"
    def get_files(self, conv_id):
        return engine.memory.get_files(int(conv_id))
    def store_file(self, conv_id, filename, content):
        engine.memory.store_file(int(conv_id), filename, content[:20000])
        return "ok"
    def get_addons(self):
        # return static addons or fetch dynamic
        try:
            with open(resource_path("addons.json"), "r") as f:
                return json.load(f)
        except:
            return {}
    def save_addon(self, category, link):
        # dynamic saving
        return "ok"
    def delete_addon(self, category, link):
        return "ok"
    def set_setting(self, key, value):
        engine.memory.set_setting(key, value)
        if key == "min_response_len":
            engine.min_response_len = int(value)
        elif key == "temperature":
            engine.temperature = float(value)
        return "ok"
    def get_setting(self, key):
        return engine.memory.get_setting(key)
    def export_conversations(self):
        convs = engine.memory.get_conversations()
        data = []
        for c in convs:
            msgs = engine.memory.get_messages(c["id"])
            data.append({"conversation": c, "messages": msgs})
        with open("export.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return "Exported to export.json"

def main():
    html_path = resource_path("index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    webview.create_window(f"CrownStar Ultimate {TIER}", html=html, js_api=API(), width=1400, height=900, min_size=(1000,700))
    webview.start()

if __name__ == "__main__":
    main()
