import unittest

from app.user_profile import wait_until_ready


class TestWaitUntilReadySlow(unittest.TestCase):
    """Медленные тесты с реальными задержками времени.
    
    Эти тесты используют реальный time.sleep(), поэтому они будут
    медленными и хорошо видны через --durations.
    """
    
    def test_ready_after_two_polls(self):
        """Тест проверяет успешное завершение после двух опросов.
        
        Реальная задержка: 2 интервала * 0.10 сек = ~0.20 сек
        """
        states = iter(["pending", "pending", "ready"])

        def check():
            return next(states, "ready")

        self.assertTrue(wait_until_ready(check, timeout=0.30, interval=0.10))

    def test_timeout(self):
        """Тест проверяет таймаут при постоянном статусе 'pending'.
        
        Реальная задержка: ~0.25 сек (время таймаута)
        """
        self.assertFalse(
            wait_until_ready(lambda: "pending", timeout=0.25, interval=0.05)
        )
    
    def test_ready_after_three_polls(self):
        """Дополнительный медленный тест для наглядности.
        
        Реальная задержка: 3 интервала * 0.15 сек = ~0.45 сек
        """
        states = iter(["pending", "pending", "pending", "ready"])

        def check():
            return next(states, "ready")

        self.assertTrue(wait_until_ready(check, timeout=0.60, interval=0.15))
    
    def test_immediate_ready(self):
        """Тест с немедленной готовностью - всё равно медленный из-за структуры.
        
        Даже при немедленной готовности функция всё равно делает
        один цикл проверки, но sleep не вызывается.
        """
        def check():
            return "ready"
        
        self.assertTrue(wait_until_ready(check, timeout=0.30, interval=0.10))
    
    def test_long_timeout_with_early_ready(self):
        """Тест с большим таймаутом, но ранним успехом.
        
        Должен завершиться быстро, но timeout большой.
        """
        states = iter(["pending", "ready"])
        
        def check():
            return next(states, "ready")
        
        self.assertTrue(wait_until_ready(check, timeout=2.0, interval=0.10))


class TestWaitUntilReadySlowEdgeCases(unittest.TestCase):
    """Дополнительные медленные тесты для пограничных случаев."""
    
    def test_exact_timeout_boundary(self):
        """Тест на границе таймаута.
        
        Проверяет поведение точно в момент таймаута.
        """
        import time
        
        start = time.time()
        result = wait_until_ready(lambda: "pending", timeout=0.10, interval=0.01)
        elapsed = time.time() - start
        
        self.assertFalse(result)
        self.assertAlmostEqual(elapsed, 0.10, delta=0.05)
    
    def test_very_short_interval(self):
        """Тест с очень коротким интервалом опроса.
        
        Больше итераций = больше времени на sleep.
        """
        states = iter(["pending"] * 10 + ["ready"])
        
        def check():
            return next(states, "pending")
        
        self.assertTrue(wait_until_ready(check, timeout=0.50, interval=0.01))
    
    def test_never_ready_long_timeout(self):
        """Тест, который ждёт до самого таймаута.
        
        Самый медленный тест из всех.
        """
        self.assertFalse(
            wait_until_ready(lambda: "pending", timeout=0.50, interval=0.05)
        )


if __name__ == "__main__":
    unittest.main()