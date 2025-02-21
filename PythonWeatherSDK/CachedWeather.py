import time


class CachedWeather:
    def __init__(self, data):
        self.data = data
        self.timestamp = time.time()

    def is_expired(self) -> bool:
        return (time.time() - self.timestamp) > 10 * 60

    def get_data(self):
        return self.data
