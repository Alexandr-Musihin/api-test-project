import pytest
import json
import os
from utils.api_client import PetstoreAPIClient
from utils.validators import validate_json_schema
from utils.helpers import load_test_data

class TestPetstoreProfessional:
    """Тесты уровня 3: Профессиональные сценарии"""
    
    @pytest.fixture
    def api_client(self):
        client = PetstoreAPIClient()
        # Добавляем кастомные заголовки
        client.add_header('X-Custom-Header', 'TestValue')
        client.add_header('Accept', 'application/json')
        return client
    
    @pytest.fixture
    def test_data(self):
        return load_test_data()
    
    def test_json_schema_validation(self, api_client, test_data):
        """Тест 9: Валидация JSON схем для успешных ответов"""
        # Загружаем схему
        with open('data/schemas/pet_schema.json', 'r') as f:
            pet_schema = json.load(f)
        
        # Создаем питомца
        pet_data = test_data['pets'][0]
        response = api_client.create_pet(pet_data)
        
        assert response.status_code == 200
        
        # Валидируем ответ по схеме
        response_data = response.json()
        is_valid, errors = validate_json_schema(response_data, pet_schema)
        
        assert is_valid, f"Schema validation failed: {errors}"
    
    def test_dependent_scenario(self, api_client, test_data):
        """Тест 10: Сценарий с зависимостями"""
        pet_data = test_data['pets'][0]
        
        # 1. Создаем питомца
        create_response = api_client.create_pet(pet_data)
        pet_id = create_response.json()['id']
        
        # 2. Изменяем статус
        updated_data = pet_data.copy()
        updated_data['id'] = pet_id
        updated_data['status'] = 'pending'
        
        update_response = api_client.update_pet(updated_data)
        assert update_response.status_code == 200
        
        # 3. Проверяем в списке по статусу
        find_response = api_client.find_pets_by_status('pending')
        assert find_response.status_code == 200
        
        pending_pets = find_response.json()
        pet_ids = [pet['id'] for pet in pending_pets]
        assert pet_id in pet_ids, f"Pet {pet_id} not found in pending pets list"
        
        # 4. Удаляем питомца
        delete_response = api_client.delete_pet(pet_id)
        assert delete_response.status_code == 200
        
        # 5. Проверяем удаление
        get_response = api_client.get_pet_by_id(pet_id)
        assert get_response.status_code == 404
    
    def test_response_headers(self, api_client, test_data):
        """Тест 11: Проверка заголовков ответов"""
        response = api_client.find_pets_by_status('available')
        
        assert response.status_code == 200
        
        # Проверяем Content-Type
        content_type = response.headers.get('Content-Type', '')
        assert 'application/json' in content_type
        
        # Проверяем наличие других важных заголовков
        assert 'Date' in response.headers
        assert 'Content-Length' in response.headers or \
               'Transfer-Encoding' in response.headers
    
    @pytest.mark.parametrize('pet_data', 
                           [item for item in load_test_data()['pets']])
    def test_parameterized_from_external_data(self, api_client, pet_data):
        """Тест 12: Параметризация через внешние данные"""
        # Тестируем создание питомца с разными наборами данных
        response = api_client.create_pet(pet_data)
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data['name'] == pet_data['name']
        assert response_data['status'] == pet_data['status']
        
        # Очистка - удаляем созданного питомца
        pet_id = response_data['id']
        api_client.delete_pet(pet_id)