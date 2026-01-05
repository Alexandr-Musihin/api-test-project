import json
import random

def generate_test_data():
    """Генерирует тестовые данные для питомца"""
    return {
        "id": random.randint(100000, 999999),
        "name": f"TestPet_{random.randint(1, 1000)}",
        "category": {
            "id": random.randint(1, 10),
            "name": random.choice(["Dogs", "Cats", "Birds", "Fish"])
        },
        "photoUrls": [
            f"https://example.com/photo_{random.randint(1, 10)}.jpg"
        ],
        "tags": [
            {
                "id": random.randint(1, 5),
                "name": f"tag_{random.randint(1, 5)}"
            }
        ],
        "status": random.choice(["available", "pending", "sold"])
    }

def load_test_data(file_path='data/test_data.json'):
    """Загружает тестовые данные из файла"""
    with open(file_path, 'r') as f:
        return json.load(f)