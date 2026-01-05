import time
import statistics
import requests

def test_api_response_time():
    """Проверяем, что API отвечает за приемлемое время"""
    times = []
    for _ in range(10):
        start = time.time()
        requests.get("https://petstore.swagger.io/v2/pet/1")
        times.append(time.time() - start)
    
    avg_time = statistics.mean(times)
    p95 = statistics.quantiles(times, n=100)[94]
    
    print(f"⏱️  Среднее время: {avg_time:.3f}с, P95: {p95:.3f}с")
    assert avg_time < 1.0, f"API слишком медленный: {avg_time:.3f}с"
    assert p95 < 2.0, f"95% запросов дольше 2 секунд: {p95:.3f}с"