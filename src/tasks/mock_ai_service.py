import random
from time import sleep


class AIService:
    def analyze_text(self, text: str) -> dict:
        sleep(random.uniform(1, 3))

        crit = ("error", "exception", "failed")
        warn = ("warning", "attention", "careful")

        if any(word in text.lower() for word in crit):
            category = "critical"
            confidence = random.uniform(0.7, 0.95)
        elif any(word in text.lower() for word in warn):
            category = "warning"
            confidence = random.uniform(0.6, 0.9)
        else:
            category = "info"
            confidence = random.uniform(0.8, 0.99)

        return {
            "category": category,
            "confidence": confidence,
            "keywords": random.sample(text.split(), min(3, len(text.split()))),
        }
