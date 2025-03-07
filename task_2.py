import time
from typing import Dict
import random

class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        self.min_interval = min_interval
        self.user_requests: Dict[str, float] = {}

    def can_send_message(self, user_id: str) -> bool:
        """Перевіряє, чи може користувач відправити повідомлення"""
        if self.min_interval <= 0:  
            return True 

        current_time = time.time()
        if user_id not in self.user_requests:
            self.user_requests[user_id] = current_time
            return True
        
        last_request_time = self.user_requests[user_id]        


        if current_time - last_request_time >= self.min_interval:
            self.user_requests[user_id] = current_time
            return True
        else:
            return False

    def record_message(self, user_id: str) -> bool:
        """Запис нового повідомлення з оновленням часу"""
        if not self.can_send_message(user_id):
            return False
        self.user_requests[user_id] = time.time()
        return True


    def time_until_next_allowed(self, user_id: str) -> float:
        """Розрахунок часу до можливості відправлення наступного повідомлення"""
        current_time = time.time()
    
        if user_id not in self.user_requests:
            return 0.0

        last_request_time = self.user_requests[user_id]
        return max(0.0, self.min_interval - (current_time - last_request_time))


def test_throttling_limiter():
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print("\\n=== Симуляція потоку повідомлень (Throttling) ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")

        # Випадкова затримка між повідомленнями
        time.sleep(random.uniform(0.1, 1.0))

    print("\\nОчікуємо 10 секунд...")
    time.sleep(10)

    print("\\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_throttling_limiter()
