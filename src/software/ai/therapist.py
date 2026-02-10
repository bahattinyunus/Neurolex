
import random
from typing import List, Dict, Any, Optional

class TherapeuticAssistant:
    QUESTIONS = [
        {"id": 0, "text": "Son iki hafta içinde kendinizi ne sıklıkla çökük, depresif veya umutsuz hissettiniz?", "options": ["Hiç", "Birkaç gün", "Günlerin yarısından fazlasında", "Neredeyse her gün"]},
        {"id": 1, "text": "Bir şeyler yapmaktan az ilgi veya zevk alma durumunuz nedir?", "options": ["Hiç", "Birkaç gün", "Günlerin yarısından fazlasında", "Neredeyse her gün"]},
        {"id": 2, "text": "Kendinizi yorgun veya enerjisiz hissetme sıklığınız nedir?", "options": ["Hiç", "Birkaç gün", "Günlerin yarısından fazlasında", "Neredeyse her gün"]},
        {"id": 3, "text": "Uykuya dalmakta zorluk çekme veya çok uyuma durumunuz?", "options": ["Hiç", "Birkaç gün", "Günlerin yarısından fazlasında", "Neredeyse her gün"]},
        {"id": 4, "text": "Kendiniz hakkında kötü hissetme veya başarısız olduğunuzu düşünme sıklığınız?", "options": ["Hiç", "Birkaç gün", "Günlerin yarısından fazlasında", "Neredeyse her gün"]},
        {"id": 5, "text": "Kendinizi endişeli veya bunalmış hissediyor musunuz?", "options": ["Hiç", "Birkaç gün", "Günlerin yarısından fazlasında", "Neredeyse her gün"]},
        {"id": 6, "text": "Günlük aktivitelere odaklanmakta ne kadar zorlanıyorsunuz?", "options": ["Hiç", "Birkaç gün", "Günlerin yarısından fazlasında", "Neredeyse her gün"]}
    ]
    
    SCORES = {"Hiç": 0, "Birkaç gün": 1, "Günlerin yarısından fazlasında": 2, "Neredeyse her gün": 3}
    
    RISK_LEVELS = {
        "happy": (0, 25),      # %0-25
        "normal": (25, 50),    # %25-50
        "sad": (50, 75),       # %50-75
        "depressed": (75, 101) # %75-100
    }
    
    # Resources adapted from source, translated/localized implies placeholders or generic links
    RESOURCES = {
        "happy": {
            "message": "Harika görünüyorsun! İçindeki bu ışığı koru.",
            "content_type": "quote",
            "content": ["Mutluluk dışarıda değil, senin içindedir!", "Küçük şeylerin tadını çıkar."]
        },
        "normal": {
            "message": "Her şey yolunda gidiyor. Motivasyonunu artırmak için bir şarkı dinle.",
            "content_type": "song",
            "content": ["https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKZFC"] # Daydreaming - Radiohead (Random placeholder) or generic relax playlist
        },
        "sad": {
            "message": "Biraz moral bozukluğu normaldir. Seni neşelendirecek bir video izle.",
            "content_type": "video",
            "content": ["https://www.youtube.com/watch?v=q6EoRBvdVPQ"] # Ying Yang Twins - Halftime (Wait, lets use something calm) -> Lofi Girl
        },
        "depressed": {
            "message": "Zor bir dönemden geçiyor olabilirsin. Bir uzmandan destek almanı öneririz.",
            "content_type": "contact",
            "content": [
                "Dr. Ayşe Yılmaz – 📞 +90 555 123 4567",
                "Dr. Mehmet Demir – 📞 +90 555 987 6543",
                "Acil Destek Hattı: 183"
            ]
        }
    }

    @classmethod
    def process_session(cls, user_responses: List[str]) -> Dict[str, Any]:
        """
        Processes the current answers.
        If incomplete, returns the next question.
        If complete, calculates score and returns recommendation.
        """
        current_index = len(user_responses)
        
        if current_index < len(cls.QUESTIONS):
            # Return Next Question
            q = cls.QUESTIONS[current_index]
            return {
                "status": "in_progress",
                "question": q["text"],
                "options": q["options"],
                "progress": current_index / len(cls.QUESTIONS)
            }
        
        # Calculate Assessment
        total_score = sum(cls.SCORES.get(r, 0) for r in user_responses)
        max_score = len(cls.QUESTIONS) * 3
        percentage = (total_score / max_score) * 100
        
        risk_level = "happy"
        for level, (low, high) in cls.RISK_LEVELS.items():
            if low <= percentage < high:
                risk_level = level
                break
                
        resource = cls.RESOURCES.get(risk_level, {})
        
        return {
            "status": "complete",
            "risk_level": risk_level,
            "score_percentage": round(percentage, 1),
            "message": resource.get("message"),
            "content_type": resource.get("content_type"),
            "content": resource.get("content")
        }
