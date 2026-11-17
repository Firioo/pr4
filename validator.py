import os

def validate_filename(filename: str) -> bool:
    """
    Проверяет имя файла на соответствие требованиям.
    Возвращает True, если имя корректно.
    Возбуждает ValueError или TypeError при нарушении.
    """
    if not isinstance(filename, str):
        raise TypeError("Имя файла должно быть строкой")

    if not filename:
        raise ValueError("Имя файла не может быть пустым")

    # 1. Проверка на наличие пути (самая первая проверка)
    if os.path.sep in filename or (os.path.altsep and os.path.altsep in filename):
        raise ValueError("Имя не должно содержать символы пути")

    # 2. Проверка на скрытый файл (начинается с точки)
    # Должна быть ДО разделения на имя и расширение
    if filename.startswith('.'):
        raise ValueError("Загрузка скрытых файлов запрещена")

    # 3. Разделяем имя и расширение (только последняя точка)
    parts = filename.rsplit('.', 1)
    base_name = parts[0]
    ext = parts[1] if len(parts) > 1 else ""

    # 4. Проверка длины (включая точку и расширение)
    if len(filename) > 64:
        raise ValueError("Имя файла превышает 64 символа")

    # 5. Проверка на двойное расширение, оканчивающееся на .exe (ДО проверки расширений)
    if '.' in base_name:
        second_ext = base_name.rsplit('.', 1)[1]
        if second_ext.lower() == "exe":
            raise ValueError("Загрузка исполняемых файлов (.exe) запрещена")

    # 6. Проверка на .exe как основное расширение (ДО проверки разрешенных)
    if ext.lower() == "exe":
        raise ValueError("Загрузка исполняемых файлов (.exe) запрещена")

    # 7. Проверка разрешенных расширений (последняя проверка)
    if ext not in ["txt", "csv"]:
        raise ValueError(f"Недопустимое расширение файла: .{ext}")

    return True