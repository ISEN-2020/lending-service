# on utilise une image Python
FROM python:3.9

# on defini le repertoire de travail
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json ./
RUN pip install -r requirements.txt


EXPOSE 5000

# Start the application
CMD ["python", "app.py"]