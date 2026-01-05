from jsonschema import validate, ValidationError

def validate_json_schema(data, schema):
    """
    Валидировать данные по JSON схеме
    
    Args:
        data: Данные для валидации
        schema: JSON схема
    
    Returns:
        tuple: (is_valid, errors)
    """
    try:
        validate(instance=data, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)