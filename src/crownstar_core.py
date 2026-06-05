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
