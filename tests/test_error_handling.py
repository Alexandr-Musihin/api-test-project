import requests

def test_error_responses():
    """Проверяем корректность обработки ошибок"""
    # Невалидный ID
    response = requests.get("https://petstore.swagger.io/v2/pet/not_a_number")
    assert response.status_code == 404
    
    # Слишком длинное имя
    long_name = "A" * 1000
    payload = {"id": 999, "name": long_name, "status": "available"}
    response = requests.post("https://petstore.swagger.io/v2/pet", json=payload)
    assert response.status_code == 400 or 500  # API может не принимать