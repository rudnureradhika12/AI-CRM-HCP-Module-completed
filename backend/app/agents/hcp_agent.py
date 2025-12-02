import os, json, asyncio, re
from typing import Dict, Any
import httpx

GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

class GroqError(Exception):
    pass

class GroqClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base = 'https://api.groq.com/v1'  # follow Groq docs; adjust if needed

    def chat_completion(self, model: str, messages: list, max_output_tokens: int = 512):
        if not self.api_key:
            raise GroqError('No GROQ_API_KEY provided')
        # Example HTTP call; user should verify against Groq SDK or REST docs
        url = f"{self.base}/chat/completions"
        headers = { 'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json' }
        payload = { 'model': model, 'messages': messages, 'max_output_tokens': max_output_tokens }
        resp = httpx.post(url, headers=headers, json=payload, timeout=30.0)
        resp.raise_for_status()
        data = resp.json()
        # try to extract text content
        content = ''
        try:
            content = data['choices'][0]['message']['content']
        except Exception:
            # fallback to raw
            content = json.dumps(data)
        return content

def simple_local_summarizer(notes: str) -> Dict[str, Any]:
    # Very small heuristic summarizer & entity extractor for offline use
    summary = notes.strip()
    if len(summary) > 300:
        summary = summary[:300].rsplit(' ',1)[0] + '...'
    # Entity extraction: crude — extract capitalized words and tokens that look like drug names (ending in -ine/-ol/-mab etc)
    tokens = re.findall(r"\b[A-Z][a-zA-Z0-9\-]{2,}\b", notes)
    drug_like = [t for t in tokens if re.search(r'(ine$|ol$|mab$|vir$|cillin$|azole$)', t.lower())]
    entities = [{'type': 'drug', 'value': d} for d in sorted(set(drug_like))]
    # If no drug_like found, include some capitalized tokens as people/orgs
    if not entities and tokens:
        entities = [{'type':'entity','value':t} for t in sorted(set(tokens))[:5]]
    sentiment = 'neutral'
    if any(w in notes.lower() for w in ['good','positive','interested','agree','ok','ok.','yes']): sentiment='positive'
    if any(w in notes.lower() for w in ['concern','not','no','negative','refuse','decline']): sentiment='negative'
    followups = []  # mock
    return {'summary': summary or '(no notes provided)', 'entities': entities, 'followups': followups, 'sentiment': sentiment}

class Tools:
    def __init__(self):
        self.groq = GroqClient(GROQ_API_KEY) if GROQ_API_KEY else None

    async def log_interaction_tool(self, payload: Dict[str, Any]):
        notes = payload.get('notes','') or ''
        # If GROQ API key present, try to call Groq; otherwise use local summarizer
        if self.groq:
            try:
                system_msg = {'role':'system', 'content': 'You are an expert life-sciences summarizer. Output ONLY valid JSON with keys: summary, entities, followups, sentiment.'}
                user_msg = {'role':'user', 'content': f"Notes: {notes}\n\nReturn JSON only."}
                content = self.groq.chat_completion(model='gemma2-9b-it', messages=[system_msg, user_msg], max_output_tokens=512)
                # try to find JSON substring
                m = re.search(r'\{.*\}', content, re.S)
                json_text = m.group(0) if m else content
                parsed = json.loads(json_text)
                return parsed
            except Exception as e:
                # fallback to local summarizer
                return simple_local_summarizer(notes)
        else:
            # local summarizer
            await asyncio.sleep(0.01)
            return simple_local_summarizer(notes)

    async def edit_interaction_tool(self, interaction_id: int, payload: Dict[str, Any]):
        notes = payload.get('notes','') or ''
        # Re-run summarizer (same logic)
        return await self.log_interaction_tool({'notes': notes})

class HCPAgent:
    def __init__(self):
        self.tools = Tools()
