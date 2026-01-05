import requests
import os

class PetstoreAPIClient:
    """Клиент для работы с Petstore API"""
    
    BASE_URL = "https://petstore.swagger.io/v2"
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def add_header(self, key, value):
        """Добавить кастомный заголовок"""
        self.headers[key] = value
    
    def _request(self, method, endpoint, **kwargs):
        """Базовый метод для выполнения запросов"""
        url = f"{self.BASE_URL}{endpoint}"
        
        # Добавляем заголовки к запросу
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers
        else:
            kwargs['headers'].update(self.headers)
        
        response = self.session.request(method, url, **kwargs)
        return response
    
    def create_pet(self, pet_data):
        """POST /pet - Создать питомца"""
        return self._request('POST', '/pet', json=pet_data)
    
    def get_pet_by_id(self, pet_id):
        """GET /pet/{petId} - Получить питомца по ID"""
        return self._request('GET', f'/pet/{pet_id}')
    
    def update_pet(self, pet_data):
        """PUT /pet - Обновить питомца"""
        return self._request('PUT', '/pet', json=pet_data)
    
    def delete_pet(self, pet_id):
        """DELETE /pet/{petId} - Удалить питомца"""
        return self._request('DELETE', f'/pet/{pet_id}')
    
    def find_pets_by_status(self, status):
        """GET /pet/findByStatus - Найти питомцев по статусу"""
        params = {'status': status}
        return self._request('GET', '/pet/findByStatus', params=params)
    
    def upload_image(self, pet_id, image_path):
        """POST /pet/{petId}/uploadImage - Загрузить изображение"""
        url = f"{self.BASE_URL}/pet/{pet_id}/uploadImage"
        
        with open(image_path, 'rb') as image_file:
            files = {'file': (os.path.basename(image_path), image_file)}
            response = self.session.post(url, files=files)
        
        return response