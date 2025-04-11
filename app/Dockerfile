FROM python:3.10.17-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY scripts/wait-for-it.sh /app/wait-for-it.sh
# RUN chmod +x /app/wait-for-it.sh
COPY . .

# Verwende das Skript, um sicherzustellen, dass die DB verfügbar ist
# CMD ./wait-for-it.sh db:5432 -- python main.py
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
