import subprocess
import sys
import unittest
import tempfile
import os
from  validator import validate_filename
from pathlib import Path

class IntegrationCliTest(unittest.TestCase):
    """Интеграционные тесты для консольного приложения."""

    def setUp(self):
        # Определяем путь к скрипту приложения
        self.script_path = Path(__file__).parents[1] / "app.py"
        # Создаем временную директорию для изолированных тестов файловой системы
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = self.temp_dir.name

    def tearDown(self):
        # Удаляем временную директорию после теста
        self.temp_dir.cleanup()

    def _run_app(self, *args):
        """Вспомогательный метод для запуска приложения с аргументами."""
        return subprocess.run(
            [sys.executable, str(self.script_path), *args],
            text=True,
            capture_output=True,
            encoding='utf-8',
            check=False
        )

    # --- Тесты через CLI ---
    def test_cli_valid_txt(self):
        result = self._run_app("valid.txt")
        self.assertEqual(result.returncode, 0)
        self.assertIn("корректно", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_cli_valid_csv(self):
        result = self._run_app("data.csv")
        self.assertEqual(result.returncode, 0)
        self.assertIn("корректно", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_cli_invalid_exe(self):
        result = self._run_app("bad.exe")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Загрузка исполняемых файлов (.exe) запрещена", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_cli_invalid_hidden(self):
        result = self._run_app(".hidden.txt")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Загрузка скрытых файлов запрещена", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_cli_invalid_too_long(self):
        long_name = "A" * 65 + ".txt"
        result = self._run_app(long_name)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Имя файла превышает 64 символа", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_cli_no_args(self):
        result = self._run_app()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Ошибка: укажите имя файла", result.stderr)
        self.assertEqual(result.stdout, "")

    # --- Тесты с использованием временных файлов (проверка на диске) ---
    def test_temp_file_txt_exists(self):
        """Проверяем, что файл с валидным именем создается во временной папке."""
        valid_filename = "test.txt"
        file_path = os.path.join(self.test_dir, valid_filename)
        
        # Создаем пустой файл
        Path(file_path).touch()
        
        # Проверяем, что файл действительно существует
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(validate_filename(valid_filename)) # Повторно используем валидатор

    def test_temp_file_invalid_exe_creation(self):
        """Проверяем, что создание файла с плохим именем не запрещено ОС, но наша валидация его отклонит."""
        invalid_filename = "malware.txt.exe"
        file_path = os.path.join(self.test_dir, invalid_filename)
        
        # Создание такого файла разрешено ОС, но наша программа должна его отклонить
        Path(file_path).touch()
        self.assertTrue(os.path.exists(file_path))
        
        # Проверяем, что валидатор выбрасывает ошибку
        with self.assertRaises(ValueError) as cm:
            validate_filename(invalid_filename)
        self.assertIn(".exe", str(cm.exception))

if __name__ == "__main__":
    unittest.main()