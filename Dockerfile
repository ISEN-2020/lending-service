# on utilise une image Python
FROM python:3.12.5

# on defini le repertoire de travail
WORKDIR /app

# Copy package.json and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


EXPOSE 8000

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
