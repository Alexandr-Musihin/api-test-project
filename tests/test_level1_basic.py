import pytest
import requests
from utils.api_client import PetstoreAPIClient
from utils.helpers import generate_test_data

class TestPetstoreBasic:
    """Тесты уровня 1: Базовые CRUD операции"""
    
    @pytest.fixture
    def api_client(self):
        return PetstoreAPIClient()
    
    @pytest.fixture
    def pet_data(self):
        return generate_test_data()
    
    def test_create_pet(self, api_client, pet_data):
        """Тест 1: Создание питомца"""
        response = api_client.create_pet(pet_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert 'id' in response_data, "Response should contain 'id' field"
        assert response_data['id'] == pet_data['id'], \
            f"ID mismatch: expected {pet_data['id']}, got {response_data['id']}"
        
        
    
    def test_get_pet_by_id(self, api_client, pet_data):
        """Тест 2: Получение питомца по ID"""
        # Сначала создаем питомца
        create_response = api_client.create_pet(pet_data)
        pet_id = create_response.json()['id']
        
        # Получаем питомца
        response = api_client.get_pet_by_id(pet_id)
        
        assert response.status_code == 200
        
        pet = response.json()
        assert pet['id'] == pet_id
        assert pet['name'] == pet_data['name']
        assert pet['status'] == pet_data['status']
    
    def test_update_pet(self, api_client, pet_data):
        """Тест 3: Обновление питомца"""
        # Создаем питомца
        create_response = api_client.create_pet(pet_data)
        pet_id = create_response.json()['id']
        
        # Обновляем данные
        updated_data = pet_data.copy()
        updated_data['name'] = "UpdatedPetName"
        updated_data['status'] = "sold"
        
        response = api_client.update_pet(updated_data)
        
        assert response.status_code == 200
        
        # Проверяем обновление
        get_response = api_client.get_pet_by_id(pet_id)
        updated_pet = get_response.json()
        
        assert updated_pet['name'] == "UpdatedPetName"
        assert updated_pet['status'] == "sold"
    
    def test_delete_pet(self, api_client, pet_data):
        """Тест 4: Удаление питомца"""
        # Создаем питомца
        create_response = api_client.create_pet(pet_data)
        pet_id = create_response.json()['id']
        
        # Удаляем питомца
        response = api_client.delete_pet(pet_id)
        
        assert response.status_code == 200
        
        # Проверяем, что питомец удален
        get_response = api_client.get_pet_by_id(pet_id)
        assert get_response.status_code == 404