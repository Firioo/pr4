import unittest
from validator import validate_filename

class TestFilenameValidator(unittest.TestCase):
    
    # Корректные данные, которые могут использоваться в нескольких тестах
    def setUp(self):
        self.valid_txt = "document.txt"
        self.valid_csv = "data.csv"
        self.long_valid_name = "A" * 60 + ".txt"  # 64 символа всего

    # --- ПОЗИТИВНЫЕ ТЕСТЫ (ожидается True) ---
    def test_valid_txt_extension(self):
        self.assertTrue(validate_filename(self.valid_txt))

    def test_valid_csv_extension(self):
        self.assertTrue(validate_filename(self.valid_csv))

    def test_valid_max_length(self):
        self.assertTrue(validate_filename(self.long_valid_name))

    def test_valid_simple_name(self):
        self.assertTrue(validate_filename("report.txt"))

    def test_regression_second_extension_exe(self):
        """Регрессия: file.exe.txt должен отклоняться (второе расширение .exe)."""
        with self.assertRaises(ValueError) as cm:
            validate_filename("file.exe.txt")
        self.assertEqual(str(cm.exception), "Загрузка исполняемых файлов (.exe) запрещена")

    # --- НЕГАТИВНЫЕ ТЕСТЫ (ожидается ValueError) ---
    def test_error_empty_name(self):
        with self.assertRaises(ValueError) as cm:
            validate_filename("")
        self.assertEqual(str(cm.exception), "Имя файла не может быть пустым")

    def test_error_forbidden_extension(self):
        with self.assertRaises(ValueError) as cm:
            validate_filename("file.pdf")
        self.assertEqual(str(cm.exception), "Недопустимое расширение файла: .pdf")

    def test_error_exe_extension(self):
        with self.assertRaises(ValueError) as cm:
            validate_filename("virus.exe")
        self.assertEqual(str(cm.exception), "Загрузка исполняемых файлов (.exe) запрещена")

    def test_error_double_extension_exe(self):
        with self.assertRaises(ValueError) as cm:
            validate_filename("malware.txt.exe")
        self.assertEqual(str(cm.exception), "Загрузка исполняемых файлов (.exe) запрещена")

    def test_error_hidden_file(self):
        with self.assertRaises(ValueError) as cm:
            validate_filename(".secret.txt")
        self.assertEqual(str(cm.exception), "Загрузка скрытых файлов запрещена")

    def test_error_path_separator_forward(self):
        with self.assertRaises(ValueError) as cm:
            validate_filename("folder/data.csv")
        self.assertEqual(str(cm.exception), "Имя не должно содержать символы пути")

    def test_error_path_separator_backward(self):
        with self.assertRaises(ValueError) as cm:
            validate_filename("C:\\folder\\data.csv")
        self.assertEqual(str(cm.exception), "Имя не должно содержать символы пути")

    def test_error_too_long_name(self):
        long_name = "A" * 65 + ".txt"
        with self.assertRaises(ValueError) as cm:
            validate_filename(long_name)
        self.assertEqual(str(cm.exception), "Имя файла превышает 64 символа")

    def test_error_name_starts_with_dot_and_no_ext(self):
        with self.assertRaises(ValueError) as cm:
            validate_filename(".hidden")
        self.assertEqual(str(cm.exception), "Загрузка скрытых файлов запрещена")

        
    # --- НЕГАТИВНЫЙ ТЕСТ (ожидается TypeError) ---
    def test_error_not_a_string(self):
        with self.assertRaises(TypeError) as cm:
            validate_filename(123)
        self.assertEqual(str(cm.exception), "Имя файла должно быть строкой")

    

if __name__ == "__main__":
    unittest.main()