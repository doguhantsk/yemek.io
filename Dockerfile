FROM python:3.11-slim

WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Veritabanını oluştur ve seed et
RUN python seed.py

# Port
EXPOSE 5000

# Uygulamayı başlat
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
