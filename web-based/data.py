import requests
import random

URL = "https://opentdb.com/api_category.php"


class QuizData():
    def __init__(self, amount, type, category_id, difficulty):
        self.parameters = {
            "amount": amount,
            "type": type,
            "category_id": category_id,
            "difficulty": difficulty
        }

    @staticmethod
    def get_categories():
        response = requests.get(url=URL)
        data = response.json()["trivia_categories"]
        categories = [(item['id'], item['name']) for item in data]
        return categories

    def get_questions(self):
        response = requests.get(
            url="https://opentdb.com/api.php", params=self.parameters)
        response.raise_for_status()
        data = response.json()["results"]
        for item in data:
            item["option"] = item["incorrect_answers"] + [item["correct_answer"]]
            random.shuffle(item["option"])
        return data
