import os
from typing import Optional
from openai import OpenAI

SYSTEM_PROMPT = "You are Jarvis, a helpful personal AI assistant."

class GPTClient:
    def __init__(self, cfg: dict):
        key = cfg.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY missing in config.json or env.")
        self.client = OpenAI(api_key=key)
        self.model = cfg.get("MODEL", "gpt-4o-mini")

    def chat(self, prompt: str, memory=None) -> str:
        context = ""
        if memory:
            recent = memory.recent(3)
            if recent:
                context = "Recent notes: " + "; ".join([m["text"] for m in recent])
        msg = [
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":f"{context}\n\nUser: {prompt}"}
        ]
        resp = self.client.chat.completions.create(model=self.model, messages=msg)
        return resp.choices[0].message.content.strip()
