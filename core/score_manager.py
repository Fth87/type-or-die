import json
import os

SCORE_FILE = "highscores.json"

class ScoreManager:
    """
    Manajer untuk menangani penyimpanan dan pemuatan skor tinggi (High Scores).
    
    Menyimpan skor dalam file JSON lokal.
    """
    @staticmethod
    def load_scores():
        """
        Memuat daftar skor dari file.

        Returns:
            list: Daftar skor (integer) yang tersimpan. Mengembalikan list kosong jika file tidak ada atau rusak.
        """
        if not os.path.exists(SCORE_FILE):
            return []
        try:
            with open(SCORE_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def get_best_score():
        """
        Mendapatkan skor tertinggi yang pernah dicapai.

        Returns:
            int: Skor tertinggi. Mengembalikan 0 jika belum ada skor.
        """
        scores = ScoreManager.load_scores()
        if scores:
            return scores[0]
        return 0

    @staticmethod
    def save_score(new_score):
        """
        Menyimpan skor baru ke dalam daftar high scores.
        
        Hanya menyimpan 5 skor tertinggi.

        Args:
            new_score (int): Skor baru yang akan disimpan.
        """
        scores = ScoreManager.load_scores()
        scores.append(new_score)
        scores.sort(reverse=True)
        scores = scores[:5] 
        with open(SCORE_FILE, 'w') as f:
            json.dump(scores, f)