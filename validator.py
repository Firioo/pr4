# validator.py
import os

def validate_filename(filename):
    if not isinstance(filename, str):
        raise TypeError("Имя файла должно быть строкой")
    
    if not filename:
        raise ValueError("Имя файла не может быть пустым")
        
    if len(filename) > 64:
        raise ValueError("Имя файла превышает 64 символа")
        
    if filename.startswith('.'):
        raise ValueError("Загрузка скрытых файлов запрещена")
        
    if "/" in filename or "\\" in filename:
        raise ValueError("Имя не должно содержать символы пути")
        
    if filename.lower().endswith('.exe'):
        raise ValueError("Загрузка исполняемых файлов (.exe) запрещена")
        
    valid_extensions = ('.txt', '.csv')
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in valid_extensions:
        raise ValueError(f"Недопустимое расширение файла: {ext}")
        
    return True