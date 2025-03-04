FROM python:3.9-slim

WORKDIR /code
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



# FROM python:3.9-slim

# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# COPY . .

# # Указываем volume для медиафайлов
# VOLUME /app/media

# CMD ["python", "main.py"]

# FROM python:3.9-slim

# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# COPY . .

# # Указываем volume для медиафайлов
# VOLUME /app/media

# CMD ["gunicorn", "django_app.wsgi:application", "--bind", "0.0.0.0:8000"]
