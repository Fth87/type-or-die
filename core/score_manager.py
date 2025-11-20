import json
import os

SCORE_FILE = "highscores.json"

class ScoreManager:
    @staticmethod
    def load_scores():
        if not os.path.exists(SCORE_FILE):
            return []
        try:
            with open(SCORE_FILE, 'r') as f:
                return json.load(f)
        except:
            return []

    @staticmethod
    def get_best_score():
        scores = ScoreManager.load_scores()
        if scores:
            return scores[0]
        return 0

    @staticmethod
    def save_score(new_score):
        scores = ScoreManager.load_scores()
        scores.append(new_score)
        scores.sort(reverse=True)
        scores = scores[:5] 
        with open(SCORE_FILE, 'w') as f:
            json.dump(scores, f)