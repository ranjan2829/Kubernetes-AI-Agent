FROM python:3.9-slim
WORKDIR /app
ENV PYTHONPATH=/app
COPY app.py /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
