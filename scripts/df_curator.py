#!/usr/bin/env python3
"""
Dark Factory – Curator
Gera ideias diárias conforme playlist do dia, máx 3 por playlist.
Ordem IA: Groq → Gemini 2.5 Flash → Gemini 2.5 Lite
"""
import os
import sys
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

import requests

# ---------- CONFIG ----------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
LIST_ID = os.getenv("LIST_ID_SUGESTOES")

TARGET_PER_PLAYLIST = 3

# Playlists por dia (0=Segunda, 6=Domingo)
PLAYLISTS = {
    0: {"nome": "Dark Mind", "emoji": "🧠", "label_id": "696d55a66e663fa22777bc27", "tema": "neurociência, psicologia sombria, hacks mentais, neuroplasticidade"},
    1: {"nome": "Dark Philosophy", "emoji": "🕯️", "label_id": "696d55bbe666b7de047c5f1b", "tema": "filosofia existencial, paradoxos, pensadores, questionamentos profundos"},
    2: {"nome": "Dark Systems", "emoji": "🕹️", "label_id": "696d55d910eca3f1a74a4c7f", "tema": "sistemas de poder, controle social, manipulação, estruturas ocultas"},
    3: {"nome": "Dark Stories", "emoji": "📖", "label_id": "696d561b5c8e4354e46cd630", "tema": "narrativas sombrias, casos reais, mistérios, histórias de superação"},
    4: {"nome": "Dark Discipline", "emoji": "⚡", "label_id": "696d56407a6eb4a93c7a29cf", "tema": "disciplina, produtividade sombria, mentalidade, hábitos atômicos"},
    5: {"nome": "Dark Consciousness", "emoji": "🌌", "label_id": "696d566a9f66fa52151ea354", "tema": "consciência, espiritualidade sombria, ego, ilusão da realidade"},
    6: {"nome": "Dark Future", "emoji": "🤖", "label_id": "696d56890c71cbd4401c35fa", "tema": "futuro distópico, IA, transhumanismo, tecnologia sombria"},
}

# ---------- IA CLIENTS ----------
class GroqClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"
    
    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "max_tokens": 2000
        }
        r = requests.post(self.url, headers=headers, json=data, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

class GeminiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.primary = "gemini-2.5-flash"
        self.fallback = "gemini-2.5-flash-lite"
    
    def generate(self, prompt: str) -> str:
        for model in [self.primary, self.fallback]:
            try:
                url = f"{self.url}/{model}:generateContent?key={self.api_key}"
                data = {"contents": [{"parts": [{"text": prompt}]}]}
                r = requests.post(url, json=data, timeout=30)
                r.raise_for_status()
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                print(f"⚠️ {model} falhou: {e}")
                continue
        raise RuntimeError("Gemini falhou em ambos modelos")

def generate_with_fallback(prompt: str) -> str:
    """Groq → Gemini Flash → Gemini Lite"""
    if GROQ_API_KEY:
        try:
            print("🔄 Tentando Groq...")
            client = GroqClient(GROQ_API_KEY)
            return client.generate(prompt)
        except Exception as e:
            print(f"⚠️ Groq falhou: {e}")
    
    if GEMINI_API_KEY:
        print("🔄 Tentando Gemini...")
        client = GeminiClient(GEMINI_API_KEY)
        return client.generate(prompt)
    
    raise RuntimeError("Nenhuma chave de API configurada")

# ---------- TRELLO ----------
def get_cards_with_labels() -> list:
    """Retorna cards com suas etiquetas."""
    url = f"https://api.trello.com/1/lists/{LIST_ID}/cards"
    params = {"key": TRELLO_KEY, "token": TRELLO_TOKEN, "fields": "name,labels"}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def count_cards_by_label(label_id: str) -> int:
    """Conta cards com etiqueta específica na lista."""
    cards = get_cards_with_labels()
    return sum(1 for card in cards if any(label["id"] == label_id for label in card.get("labels", [])))

def create_card(name: str, desc: str, label_ids: list) -> dict:
    url = "https://api.trello.com/1/cards"
    data = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "idList": LIST_ID,
        "name": name,
        "desc": desc,
        "pos": "top",
        "idLabels": ",".join(label_ids)
    }
    r = requests.post(url, data=data, timeout=15)
    r.raise_for_status()
    return r.json()

# ---------- PROMPTS ----------
def get_prompt(playlist: dict, n: int) -> str:
    return f"""Você é um roteirista experiente de YouTube, não um robô. Escreva como uma pessoa real, com voz própria, curiosidade genuína e tom conversacional.

Playlist: {playlist['emoji']} {playlist['nome']}
Tema: {playlist['tema']}

Crie {n} ideia(s) de vídeo que:
- Pareça escrito por um humano, não IA
- Use linguagem natural, gírias leves, imperfeições aceitáveis
- Provoca curiosidade imediata (clickbait ético)
- Tenha ângulo único, não genérico

Para cada ideia, devolva exatamente:
Título: <máx 80 caracteres, instigante, natural>
Sinopse: <2 frases, tom de "e se eu te disser que...">
Hook: <primeiros 5 segundos do vídeo, como você falaria>

Separe ideias com ---
Lembre: natural > perfeito. Escreva como você falaria com um amigo intrigado."""

# ---------- PARSER ----------
def parse_ideas(text: str, n: int) -> list:
    ideas = []
    blocks = [b.strip() for b in text.split("---") if b.strip()]
    
    for block in blocks[:n]:
        idea = {"titulo": "", "sinopse": "", "hook": ""}
        for line in block.splitlines():
            line = line.strip()
            if line.startswith("Título:"):
                idea["titulo"] = line.replace("Título:", "").strip()
            elif line.startswith("Sinopse:"):
                idea["sinopse"] = line.replace("Sinopse:", "").strip()
            elif line.startswith("Hook:"):
                idea["hook"] = line.replace("Hook:", "").strip()
        if idea["titulo"]:
            ideas.append(idea)
    
    return ideas

# ---------- MAIN ----------
def main():
    hoje = datetime.now()
    dia_semana = hoje.weekday()
    playlist = PLAYLISTS[dia_semana]
    
    print(f"[{hoje.strftime('%d/%m/%Y')}] Dark Factory Curator")
    print(f"📅 Playlist de hoje: {playlist['emoji']} {playlist['nome']}")
    
    # Conta apenas cards da playlist do dia
    atual = count_cards_by_label(playlist["label_id"])
    faltam = max(0, TARGET_PER_PLAYLIST - atual)
    
    print(f"📊 Cards {playlist['nome']}: {atual}/{TARGET_PER_PLAYLIST}")
    
    if faltam == 0:
        print(f"✅ Já existem {atual} cards de {playlist['nome']}. Nada a fazer.")
        return
    
    print(f"📊 Faltam {faltam} card(s) de {playlist['nome']}")
    
    prompt = get_prompt(playlist, faltam)
    response = generate_with_fallback(prompt)
    ideas = parse_ideas(response, faltam)
    
    if len(ideas) < faltam:
        print("❌ IA não gerou ideias suficientes")
        sys.exit(1)
    
    for i, idea in enumerate(ideas, 1):
        titulo = f"{atual + i}. {idea['titulo']}"
        desc = f"Sinopse: {idea['sinopse']}\n\nHook: {idea['hook']}\n\nGerado em {hoje.strftime('%d/%m/%Y')} | Playlist: {playlist['nome']}"
        card = create_card(titulo, desc, [playlist["label_id"]])
        print(f"✅ Card criado: {card.get('shortUrl')} | Etiqueta: {playlist['nome']}")

if __name__ == "__main__":
    main()