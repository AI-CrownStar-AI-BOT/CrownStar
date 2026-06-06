# crownstar_core.py – Cognitive Engine
import asyncio, aiohttp, re, random, sqlite3
from collections import defaultdict
from datetime import datetime

class MarkovChain:
    def __init__(self, order=2):
        self.order = order
        self.chain = defaultdict(list)
        self.builtin = [
            "CrownStar is a sovereign cognitive engine.",
            "The internet contains endless knowledge.",
            "Gamma bursts enhance reasoning.",
            "Lateral thinking solves complex problems."
        ]
        for t in self.builtin: self.train(t)
    def train(self, text):
        words = text.lower().split()
        if len(words) < self.order+1: return
        for i in range(len(words)-self.order):
            key = tuple(words[i:i+self.order])
            self.chain[key].append(words[i+self.order])
    def generate(self, max_words=30):
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
        self.conn.execute('''CREATE TABLE IF NOT EXISTS memory
                            (id INTEGER PRIMARY KEY, query TEXT, response TEXT, timestamp TEXT)''')
    def store(self, query, response):
        self.conn.execute("INSERT INTO memory (query, response, timestamp) VALUES (?,?,?)",
                          (query, response, datetime.now().isoformat()))
        self.conn.commit()
    def recall(self, query):
        cur = self.conn.execute("SELECT response FROM memory WHERE query LIKE ? ORDER BY timestamp DESC LIMIT 1",
                                (f'%{query}%',))
        row = cur.fetchone()
        return row[0] if row else None

class CrownStarCognitive:
    def __init__(self, tier="Free"):
        self.tier = tier
        self.markov = MarkovChain()
        self.cortex = WebCortex()
        self.memory = CrownStarMemory()
    async def think(self, query):
        mem = self.memory.recall(query)
        if mem:
            return f"⚡ CrownStar ({self.tier}) [recalled]: {mem}"
        domains = re.findall(r'\b([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', query)
        if not domains: domains = ["example.com"]
        all_texts = []
        for domain in domains[:2]:
            all_texts.extend(await self.cortex.harvest(domain, query))
        if not all_texts: all_texts = self.markov.builtin
        for txt in all_texts:
            if txt and len(txt) > 10: self.markov.train(txt)
        answer = self.markov.generate(max_words=40)
        if not answer or len(answer) < 10: answer = random.choice(self.markov.builtin)
        self.memory.store(query, answer)
        return f"⚡ CrownStar ({self.tier}): {answer}"
