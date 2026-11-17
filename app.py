import sys
import io
from validator import validate_filename


# Принудительно устанавливаем UTF-8 для stdout и stderr
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def main():
    if len(sys.argv) < 2:
        print("Ошибка: укажите имя файла для проверки.", file=sys.stderr)
        return 1

    filename = sys.argv[1]

    try:
        if validate_filename(filename):
            print(f"Имя файла '{filename}' корректно.")
            return 0
    except (ValueError, TypeError) as e:
        print(f"Ошибка валидации: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())