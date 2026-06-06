# llm_wrapper.py – Local LLM with IQ/EQ sliders
import os, json, threading
from pathlib import Path
import requests

class CrownStarLLM:
    def __init__(self):
        self.settings = {"min_length": 50, "iq": 70, "eq": 60, "personality": "friendly", "language": "auto"}
        self.llm = None
        self._load_model()
    def _load_model(self):
        model_path = Path(__file__).parent.parent / "models" / "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
        if not model_path.exists():
            print("Downloading model (2.1 GB)...")
            model_path.parent.mkdir(parents=True, exist_ok=True)
            url = "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf"
            r = requests.get(url, stream=True)
            with open(model_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk: f.write(chunk)
        from llama_cpp import Llama
        self.llm = Llama(str(model_path), n_ctx=4096, n_threads=4, verbose=False)
    def _build_prompt(self, query, history=""):
        temp = 0.1 + (self.settings["iq"] / 100) * 1.4
        emotion = "neutral" if self.settings["eq"] < 30 else ("warm" if self.settings["eq"] < 70 else "highly empathetic")
        pers = self.settings["personality"]
        lang = self.settings["language"]
        if lang == "auto":
            lang_inst = "Respond in the same language as the user."
        else:
            lang_inst = f"Respond only in {lang}."
        sys_prompt = f"You are CrownStar. Personality: {pers}. Emotional tone: {emotion}. {lang_inst} Be ethical and helpful. Minimum length: {self.settings['min_length']} words."
        return f"<|start_header_id|>system<|end_header_id|>\n{sys_prompt}\n<|eot_id|>\n{history}\n<|start_header_id|>user<|end_header_id|>\n{query}\n<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>\n", temp
    def think(self, query, history=""):
        if self.llm is None:
            return "AI engine not ready."
        prompt, temp = self._build_prompt(query, history)
        resp = self.llm(prompt, max_tokens=2048, temperature=temp, top_p=0.9, stop=["<|eot_id|>"], echo=False)
        ans = resp['choices'][0]['text'].strip()
        # Enforce minimum length (simple repeat if needed)
        words = ans.split()
        while len(words) < self.settings["min_length"] and len(ans) < 6000:
            extra = self.llm(ans, max_tokens=200, temperature=temp)['choices'][0]['text'].strip()
            ans += " " + extra
            words = ans.split()
        return ans
    def update_settings(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.settings:
                self.settings[k] = v
        return "Settings updated"
