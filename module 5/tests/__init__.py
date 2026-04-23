# tests/__init__.py
import os
import pathlib
import unittest

def load_tests(loader, standard_tests, pattern):
    root = pathlib.Path(__file__).resolve().parent
    top = root.parent  # project/
    
    file_pattern = pattern or "test*.py"
    suite = unittest.TestSuite()
    
    # Всегда unit-тесты
    unit_dir = root / "unit"
    if unit_dir.exists():
        suite.addTests(
            loader.discover(
                start_dir=str(unit_dir),
                pattern=file_pattern,
                top_level_dir=str(top)
            )
        )
    
    # Интеграционные — только по флагу
    if os.getenv("RUN_INTEGRATION") == "1":
        integration_dir = root / "integration"
        if integration_dir.exists():
            suite.addTests(
                loader.discover(
                    start_dir=str(integration_dir),
                    pattern=file_pattern,
                    top_level_dir=str(top)
                )
            )
    
    return suite
