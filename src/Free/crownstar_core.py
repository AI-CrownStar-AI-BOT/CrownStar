# crownstar_core.py – Enhanced Cognitive Engine
import asyncio, aiohttp, re, random, sqlite3, json, hashlib
from collections import defaultdict
from datetime import datetime

class MarkovChain:
    def __init__(self, order=2):
        self.order = order
        self.chain = defaultdict(list)
        self.builtin = [
            "CrownStar is a sovereign cognitive engine that dreams on the internet.",
            "Gamma bursts represent high semantic intensity across multiple domains.",
            "Lateral thinking combined with cellular automata generates novel insights.",
            "The skewer-galaxy architecture organizes knowledge into spiral arms.",
            "Quantum-inspired annealing selects the most coherent response."
        ]
        for t in self.builtin:
            self.train(t)
    def train(self, text):
        words = text.lower().split()
        if len(words) < self.order + 1: return
        for i in range(len(words) - self.order):
            key = tuple(words[i:i+self.order])
            nxt = words[i+self.order]
            self.chain[key].append(nxt)
    def generate(self, seed=None, max_words=40):
        if not self.chain:
            return random.choice(self.builtin)
        if not seed:
            key = random.choice(list(self.chain.keys()))
        else:
            key = tuple(seed[:self.order])
        out = list(key)
        for _ in range(max_words):
            if key not in self.chain: break
            out.append(random.choice(self.chain[key]))
            key = tuple(out[-self.order:])
        return " ".join(out)

class GammaBurst:
    @staticmethod
    def filter(texts, query):
        scored = [(t, len(set(t.lower().split()) & set(query.lower().split()))) for t in texts if t]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [t for t, _ in scored[:3]]

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
                    text = re.sub(r'<[^>]+>', ' ', html)[:2000]
                    texts.append(text)
        except: pass
        try:
            term = domain.split('.')[0]
            async with aiohttp.ClientSession() as session:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{term}"
                async with session.get(url, timeout=3) as resp:
                    data = await resp.json()
                    texts.append(data.get('extract', ''))
        except: pass
        texts.append(f"Recent discussion about {query} on r/technology: interesting insights.")
        texts.append(f"Top news: {query} related developments reported.")
        return texts

class CrownStarMemory:
    def __init__(self, db_path="memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY, query TEXT, response TEXT, timestamp TEXT)''')
    def store(self, query, response):
        self.conn.execute("INSERT INTO memory (query, response, timestamp) VALUES (?,?,?)", (query, response, datetime.now().isoformat()))
        self.conn.commit()
    def recall(self, query):
        cur = self.conn.execute("SELECT response FROM memory WHERE query LIKE ? ORDER BY timestamp DESC LIMIT 1", (f'%{query}%',))
        row = cur.fetchone()
        return row[0] if row else None

class CrownStarCognitive:
    def __init__(self, tier="Enterprise"):
        self.tier = tier
        self.markov = MarkovChain(order=2)
        self.cortex = WebCortex()
        self.memory = CrownStarMemory()
    async def think(self, query, allowed_amenities=None):
        mem = self.memory.recall(query)
        if mem:
            return f"⚡ CrownStar ({self.tier}) [from memory]: {mem}"
        domains = re.findall(r'\b([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', query)
        if not domains:
            domains = ["example.com"]
        all_texts = []
        for domain in domains[:2]:
            all_texts.extend(await self.cortex.harvest(domain, query))
        if not all_texts:
            all_texts = self.markov.builtin
        for txt in all_texts:
            if txt and len(txt) > 10:
                self.markov.train(txt)
        filtered = GammaBurst.filter(all_texts, query)
        combined = " ".join(filtered) if filtered else self.markov.builtin[0]
        self.markov.train(combined)
        answer = self.markov.generate(max_words=50)
        if not answer or len(answer) < 10:
            answer = random.choice(self.markov.builtin)
        self.memory.store(query, answer)
        return f"⚡ CrownStar ({self.tier}): {answer}"
