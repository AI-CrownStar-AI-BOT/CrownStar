# crownstar_core.py – Ultimate Cognitive Engine v6.0
import asyncio, aiohttp, re, random, sqlite3, json, os, sys, hashlib, time, math
from collections import defaultdict, Counter
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import traceback

# ------------------------------------------------------------------
# Advanced Markov Chain with variable order and backoff smoothing
# ------------------------------------------------------------------
class AdaptiveMarkov:
    def __init__(self, max_order=5):
        self.max_order = max_order
        self.chains = [defaultdict(Counter) for _ in range(max_order+1)]  # order 1..max_order
        self.total_tokens = 0
        self.builtin = [
            "CrownStar is a sovereign cognitive engine that dreams on the internet.",
            "The internet contains endless knowledge waiting to be discovered.",
            "Gamma bursts represent moments of high semantic intensity.",
            "Lateral thinking solves problems that linear logic cannot.",
            "Your question reveals deep insight – let me elaborate.",
            "I have harvested fresh data from multiple sources to answer you thoroughly.",
            "The universe of information is vast, but I navigate it with precision."
        ]
        for text in self.builtin:
            self.train(text)

    def tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

    def train(self, text: str):
        tokens = self.tokenize(text)
        if len(tokens) < 2:
            return
        for n in range(1, self.max_order+1):
            for i in range(len(tokens)-n):
                context = tuple(tokens[i:i+n])
                next_token = tokens[i+n]
                self.chains[n][context][next_token] += 1
        self.total_tokens += len(tokens)

    def generate(self, seed_tokens: List[str] = None, max_words: int = 100) -> str:
        if self.total_tokens == 0:
            return random.choice(self.builtin)
        if seed_tokens is None or len(seed_tokens) == 0:
            # start with a random context from the highest order that exists
            for order in range(self.max_order, 0, -1):
                if self.chains[order]:
                    contexts = list(self.chains[order].keys())
                    context = random.choice(contexts)
                    break
            else:
                return random.choice(self.builtin)
        else:
            # try to find longest matching context
            context = None
            for order in range(min(self.max_order, len(seed_tokens)), 0, -1):
                cand = tuple(seed_tokens[-order:])
                if cand in self.chains[order]:
                    context = cand
                    break
            if context is None:
                # fallback to highest order random
                for order in range(self.max_order, 0, -1):
                    if self.chains[order]:
                        context = random.choice(list(self.chains[order].keys()))
                        break
                if context is None:
                    return random.choice(self.builtin)
        output = list(context) if isinstance(context, tuple) else []
        for _ in range(max_words - len(output)):
            order = len(context)
            if order == 0 or context not in self.chains[order]:
                # backoff to lower order
                found = False
                for o in range(order-1, 0, -1):
                    if o <= len(output) and tuple(output[-o:]) in self.chains[o]:
                        context = tuple(output[-o:])
                        found = True
                        break
                if not found:
                    break
            next_tokens = self.chains[len(context)][context]
            if not next_tokens:
                break
            # weighted random choice
            candidates = list(next_tokens.keys())
            weights = list(next_tokens.values())
            next_word = random.choices(candidates, weights=weights, k=1)[0]
            output.append(next_word)
            context = tuple(output[-self.max_order:])
        return " ".join(output)

# ------------------------------------------------------------------
# Web Cortex – Multi-source harvester
# ------------------------------------------------------------------
class WebCortex:
    def __init__(self):
        self.session = None
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CrownStar/6.0"

    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(headers={"User-Agent": self.user_agent})
        return self.session

    async def harvest(self, query: str, max_sources: int = 5) -> List[str]:
        texts = []
        # 1. DuckDuckGo Lite (HTML scrape)
        try:
            session = await self.get_session()
            url = f"https://lite.duckduckgo.com/lite/?q={query.replace(' ', '+')}"
            async with session.get(url, timeout=8) as resp:
                html = await resp.text()
                # extract result snippets (simple regex)
                snippets = re.findall(r'<tr class="result-snippet">.*?<td>(.*?)</td>', html, re.DOTALL)
                for s in snippets[:max_sources]:
                    clean = re.sub(r'<[^>]+>', '', s).strip()
                    if clean:
                        texts.append(clean)
        except:
            pass
        # 2. Wikipedia API
        try:
            session = await self.get_session()
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    extract = data.get('extract', '')
                    if extract:
                        texts.append(extract[:1500])
        except:
            pass
        # 3. RSS feeds (example: Hacker News)
        try:
            session = await self.get_session()
            url = "https://hnrss.org/newest?q=" + query.replace(' ', '+')
            async with session.get(url, timeout=5) as resp:
                xml = await resp.text()
                titles = re.findall(r'<title>(.*?)</title>', xml)[1:6]
                for t in titles:
                    texts.append(t)
        except:
            pass
        # 4. DNS TXT (for domain in query)
        domains = re.findall(r'\b([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', query)
        if domains:
            try:
                import dns.resolver
                answers = dns.resolver.resolve(domains[0], 'TXT')
                for r in answers:
                    txt = str(r).strip('"')
                    if txt and len(txt) > 20:
                        texts.append(txt[:1000])
            except:
                pass
        # 5. NewsAPI mock (free tier placeholder) – uses a public RSS aggregator
        try:
            session = await self.get_session()
            url = f"https://rss.news.yahoo.com/rss/{query.replace(' ', '%20')}"
            async with session.get(url, timeout=5) as resp:
                xml = await resp.text()
                items = re.findall(r'<description>(.*?)</description>', xml)[:3]
                for it in items:
                    clean = re.sub(r'<[^>]+>', '', it).strip()
                    if clean:
                        texts.append(clean)
        except:
            pass
        # deduplicate and limit
        unique = list(dict.fromkeys(texts))
        return unique[:max_sources*2]

    async def close(self):
        if self.session:
            await self.session.close()

# ------------------------------------------------------------------
# Persistent Memory with Full-Text Search and Tags
# ------------------------------------------------------------------
class CrownMemory:
    def __init__(self, db_path="memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute('''CREATE TABLE IF NOT EXISTS conversations
            (id INTEGER PRIMARY KEY, title TEXT, created TEXT, updated TEXT, tags TEXT)''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS messages
            (id INTEGER PRIMARY KEY, conv_id INTEGER, role TEXT, content TEXT, timestamp TEXT, embedding TEXT)''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS files
            (id INTEGER PRIMARY KEY, conv_id INTEGER, filename TEXT, content TEXT, timestamp TEXT)''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS settings
            (key TEXT PRIMARY KEY, value TEXT)''')
        self.conn.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(content, content= messages, content_rowid=id)''')
        self.conn.commit()

    def create_conversation(self, title: str, tags: str = "") -> int:
        ts = datetime.now().isoformat()
        cur = self.conn.execute("INSERT INTO conversations (title, created, updated, tags) VALUES (?,?,?,?)",
                                (title, ts, ts, tags))
        self.conn.commit()
        return cur.lastrowid

    def get_conversations(self) -> List[Dict]:
        cur = self.conn.execute("SELECT id, title, created, updated, tags FROM conversations ORDER BY updated DESC")
        rows = cur.fetchall()
        return [{"id": r[0], "title": r[1], "created": r[2], "updated": r[3], "tags": r[4]} for r in rows]

    def store_message(self, conv_id: int, role: str, content: str):
        ts = datetime.now().isoformat()
        self.conn.execute("INSERT INTO messages (conv_id, role, content, timestamp) VALUES (?,?,?,?)",
                          (conv_id, role, content, ts))
        self.conn.execute("UPDATE conversations SET updated=? WHERE id=?", (ts, conv_id))
        self.conn.commit()
        # update FTS
        self.conn.execute("INSERT INTO messages_fts(rowid, content) VALUES (last_insert_rowid(), ?)", (content,))
        self.conn.commit()

    def get_messages(self, conv_id: int) -> List[Dict]:
        cur = self.conn.execute("SELECT role, content, timestamp FROM messages WHERE conv_id=? ORDER BY id", (conv_id,))
        return [{"role": r[0], "content": r[1], "timestamp": r[2]} for r in cur.fetchall()]

    def search_messages(self, query: str, limit: int = 10) -> List[Dict]:
        cur = self.conn.execute("SELECT rowid, content FROM messages_fts WHERE messages_fts MATCH ? ORDER BY rank LIMIT ?", (query, limit))
        return [{"id": r[0], "content": r[1]} for r in cur.fetchall()]

    def store_file(self, conv_id: int, filename: str, content: str):
        self.conn.execute("INSERT INTO files (conv_id, filename, content, timestamp) VALUES (?,?,?,?)",
                          (conv_id, filename, content, datetime.now().isoformat()))
        self.conn.commit()

    def get_files(self, conv_id: int) -> List[Dict]:
        cur = self.conn.execute("SELECT filename, content, timestamp FROM files WHERE conv_id=?", (conv_id,))
        return [{"filename": r[0], "content": r[1][:500], "timestamp": r[2]} for r in cur.fetchall()]

    def get_setting(self, key: str, default: str = None) -> str:
        cur = self.conn.execute("SELECT value FROM settings WHERE key=?", (key,))
        row = cur.fetchone()
        return row[0] if row else default

    def set_setting(self, key: str, value: str):
        self.conn.execute("REPLACE INTO settings (key, value) VALUES (?,?)", (key, value))
        self.conn.commit()

# ------------------------------------------------------------------
# Main Cognitive Engine
# ------------------------------------------------------------------
class CrownStarCognitive:
    def __init__(self, tier: str = "Free"):
        self.tier = tier
        self.markov = AdaptiveMarkov(max_order=5)
        self.cortex = WebCortex()
        self.memory = CrownMemory()
        self.min_response_len = int(self.memory.get_setting("min_response_len", "300"))
        self.temperature = float(self.memory.get_setting("temperature", "0.8"))

    async def think(self, query: str, conv_id: int = 1, min_len: int = None, tags: str = "") -> str:
        if min_len is None:
            min_len = self.min_response_len
        # 1. Check memory for similar query (full-text search)
        similar = self.memory.search_messages(query, limit=1)
        if similar and random.random() < 0.3:
            # recall previous answer
            return f"💎 CrownStar ({self.tier}) [recalled]: {similar[0]['content'][:500]}"
        # 2. Harvest internet
        harvested = await self.cortex.harvest(query, max_sources=8)
        # 3. Train Markov on harvested texts + builtin
        all_texts = harvested + self.markov.builtin
        for txt in all_texts:
            if txt and len(txt) > 20:
                self.markov.train(txt)
        # 4. Generate answer
        seed = self.markov.tokenize(query)[-self.markov.max_order:]
        answer = self.markov.generate(seed_tokens=seed, max_words=120)
        if not answer or len(answer) < 20:
            answer = random.choice(self.markov.builtin)
        # 5. Enforce minimum length (ethical padding)
        if len(answer) < min_len:
            needed = min_len - len(answer)
            padding = " " + " ".join(self.markov.builtin) + " "
            while len(answer) < min_len:
                answer += padding[:min_len - len(answer)]
        # 6. Store conversation
        self.memory.store_message(conv_id, "user", query)
        self.memory.store_message(conv_id, "assistant", answer)
        return f"💎 CrownStar ({self.tier}): {answer}"

    async def close(self):
        await self.cortex.close()
