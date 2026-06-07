# crownstar_core.py – Proprietary Cognitive Engine v5.2.0
import asyncio, aiohttp, re, random, sqlite3, sys, os
from collections import defaultdict
from datetime import datetime

class MarkovChain:
    def __init__(self, order=3):
        self.order = order
        self.chain = defaultdict(list)
        self.builtin = [
            "CrownStar is a sovereign cognitive engine.",
            "The internet contains endless knowledge.",
            "Gamma bursts enhance reasoning.",
            "Lateral thinking solves complex problems.",
            "Your question is insightful and deserves a thorough answer.",
            "Let me elaborate further to ensure complete understanding."
        ]
        for t in self.builtin: self.train(t)
    def train(self, text):
        words = text.lower().split()
        if len(words) < self.order+1: return
        for i in range(len(words)-self.order):
            key = tuple(words[i:i+self.order])
            self.chain[key].append(words[i+self.order])
    def generate(self, max_words=60):
        if not self.chain: return random.choice(self.builtin)
        key = random.choice(list(self.chain.keys()))
        out = list(key)
        for _ in range(max_words):
            if key not in self.chain: break
            out.append(random.choice(self.chain[key]))
            key = tuple(out[-self.order:])
        return " ".join(out)

class WebCortex:
    async def harvest(self, domain, query):
        texts = []
        try:
            import dns.resolver
            answers = dns.resolver.resolve(domain, 'TXT')
            texts.extend([str(r).strip('"') for r in answers])
        except: pass
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://{domain}", timeout=3) as resp:
                    html = await resp.text()
                    texts.append(re.sub(r'<[^>]+>', ' ', html)[:2000])
        except: pass
        try:
            term = domain.split('.')[0]
            async with aiohttp.ClientSession() as session:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{term}"
                async with session.get(url, timeout=3) as resp:
                    data = await resp.json()
                    texts.append(data.get('extract', ''))
        except: pass
        texts.append(f"Recent insights about {query} from online communities.")
        return texts

class CrownStarMemory:
    def __init__(self, db_path="memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS conversations
            (id INTEGER PRIMARY KEY, title TEXT, created TEXT)''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS messages
            (id INTEGER PRIMARY KEY, conv_id INTEGER, role TEXT, content TEXT, timestamp TEXT)''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS files
            (id INTEGER PRIMARY KEY, conv_id INTEGER, filename TEXT, content TEXT, timestamp TEXT)''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS settings
            (key TEXT PRIMARY KEY, value TEXT)''')
        self.conn.commit()
    def store_message(self, conv_id, role, content):
        ts = datetime.now().isoformat()
        self.conn.execute("INSERT INTO messages (conv_id, role, content, timestamp) VALUES (?,?,?,?)",
                          (conv_id, role, content, ts))
        self.conn.commit()
    def get_messages(self, conv_id):
        cur = self.conn.execute("SELECT role, content FROM messages WHERE conv_id=? ORDER BY id", (conv_id,))
        return cur.fetchall()
    def store_file(self, conv_id, filename, content):
        self.conn.execute("INSERT INTO files (conv_id, filename, content, timestamp) VALUES (?,?,?,?)",
                          (conv_id, filename, content, datetime.now().isoformat()))
        self.conn.commit()
    def get_files(self, conv_id):
        cur = self.conn.execute("SELECT filename, content FROM files WHERE conv_id=?", (conv_id,))
        return cur.fetchall()
    def get_setting(self, key, default=None):
        cur = self.conn.execute("SELECT value FROM settings WHERE key=?", (key,))
        row = cur.fetchone()
        return row[0] if row else default
    def set_setting(self, key, value):
        self.conn.execute("REPLACE INTO settings (key, value) VALUES (?,?)", (key, value))
        self.conn.commit()

class CrownStarCognitive:
    def __init__(self, tier="Free"):
        self.tier = tier
        self.markov = MarkovChain()
        self.cortex = WebCortex()
        self.memory = CrownStarMemory()
        self.min_response_len = int(self.memory.get_setting("min_response_len", "200"))

    async def think(self, query, conv_id=1, min_len=None):
        if min_len is None: min_len = self.min_response_len
        domains = re.findall(r'\b([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', query)
        if not domains: domains = ["example.com"]
        all_texts = []
        for domain in domains[:2]:
            all_texts.extend(await self.cortex.harvest(domain, query))
        if not all_texts: all_texts = self.markov.builtin
        for txt in all_texts:
            if txt and len(txt) > 10: self.markov.train(txt)
        answer = self.markov.generate(max_words=80)
        if not answer or len(answer) < 10: answer = random.choice(self.markov.builtin)
        if len(answer) < min_len:
            needed = min_len - len(answer)
            padding = " " + " ".join(self.markov.builtin) + " "
            while len(answer) < min_len:
                answer += padding[:min_len - len(answer)]
        self.memory.store_message(conv_id, "assistant", answer)
        return f"💎 CrownStar ({self.tier}): {answer}"
