import pytest
import requests
import os
from utils.api_client import PetstoreAPIClient
from utils.helpers import generate_test_data

class TestPetstoreAdvanced:
    """Тесты уровня 2: Продвинутые сценарии"""
    
    @pytest.fixture
    def api_client(self):
        return PetstoreAPIClient()
    
    @pytest.fixture
    def pet_data(self):
        return generate_test_data()
    
    def test_negative_create_pet_invalid_data(self, api_client):
        """Тест 5: Создание питомца с невалидными данными"""
        invalid_data = {
            "id": "not_a_number",  # Строка вместо числа
            "name": "TestPet",
            "photoUrls": []
        }
        
        response = api_client.create_pet(invalid_data)
        
        # API может вернуть 400 или 500 при невалидных данных
        assert response.status_code in [400, 500], \
            f"Expected 400 or 500 for invalid data, got {response.status_code}"
    
    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_find_pets_by_status(self, api_client, status):
        """Тест 6: Поиск питомцев по статусу"""
        response = api_client.find_pets_by_status(status)
        
        assert response.status_code == 200
        
        pets = response.json()
        
        # Проверяем, что все возвращенные питомцы имеют запрошенный статус
        if pets:  # Если список не пустой
            for pet in pets:
                assert pet['status'] == status, \
                    f"Pet {pet['id']} has status {pet['status']}, expected {status}"
    
    def test_upload_pet_image(self, api_client, pet_data):
        """Тест 7: Загрузка изображения для питомца"""
        # Создаем питомца
        create_response = api_client.create_pet(pet_data)
        pet_id = create_response.json()['id']
        
        # Создаем тестовый файл изображения
        test_image_path = "test_image.jpg"
        with open(test_image_path, 'w') as f:
            f.write("test image content")
        
        try:
            # Загружаем изображение
            response = api_client.upload_image(pet_id, test_image_path)
            
            assert response.status_code == 200
            
            response_data = response.json()
            assert 'message' in response_data
            assert 'File uploaded' in response_data['message']
            
        finally:
            # Удаляем тестовый файл
            if os.path.exists(test_image_path):
                os.remove(test_image_path)
    
    def test_get_nonexistent_pet(self, api_client):
        """Тест 8: Получение несуществующего питомца"""
        non_existent_id = 999999999
        
        response = api_client.get_pet_by_id(non_existent_id)
        
        assert response.status_code == 404
        
        error_data = response.json()
        assert 'message' in error_data
        assert 'Pet not found' in error_data['message'] or \
               str(non_existent_id) in error_data['message']