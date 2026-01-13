FROM python:3.9-slim

# Fix for 2026: Use libgl1 and libglx-mesa0 instead of the obsolete libgl1-mesa-glx
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglx-mesa0 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Continue with your build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "main.py"]
