FROM python:3.12.7-slim
WORKDIR /app
COPY . /app
CMD ["python", "report.py", "data.json.example"]