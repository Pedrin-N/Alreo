# Alreo — imagem de DESENVOLVIMENTO (TCC I).
# A imagem de produção (TCC II) virá depois da refatoração multiusuário.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ALREO_HOST=0.0.0.0 \
    ALREO_PORT=5000 \
    ALREO_DEBUG=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
