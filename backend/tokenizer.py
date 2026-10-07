from typing import List, Dict, Any
import tiktoken

class TokenizerManager:
    def __init__(self, encoding_name: str = "cl100k_base"):
        try:
            self.encoder = tiktoken.get_encoding(encoding_name)
        except Exception:
            self.encoder = tiktoken.get_encoding("gpt2")

    def tokenize_text(self, text: str, max_preview_tokens: int = 40) -> Dict[str, Any]:
        """Realiza tokenização explícita com inspeção de tokens para fins didáticos"""
        token_ids = self.encoder.encode(text)
        total_tokens = len(token_ids)
        
        # Decomposição dos primeiros N tokens em strings legíveis
        token_breakdown = []
        for tid in token_ids[:max_preview_tokens]:
            try:
                decoded_token = self.encoder.decode([tid])
            except Exception:
                decoded_token = "<byte>"
            token_breakdown.append({
                "id": tid,
                "token": decoded_token
            })

        return {
            "total_tokens": total_tokens,
            "char_count": len(text),
            "ratio_chars_per_token": round(len(text) / total_tokens, 2) if total_tokens > 0 else 0,
            "preview_tokens": token_breakdown,
            "token_ids_sample": token_ids[:20]
        }

tokenizer = TokenizerManager()
