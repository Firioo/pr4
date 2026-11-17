import sys
import json

def generate_report(data):
    if not data:
        return {"count": 0, "average": 0}
    return {"count": len(data), "average": sum(data) / len(data)}

def main():
    if len(sys.argv) < 2:
        print("Ошибка: укажите путь к JSON файлу.", file=sys.stderr)
        return 1
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
        result = generate_report(data)
        print(f"Отчет сформирован: {result}")
        return 0
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())