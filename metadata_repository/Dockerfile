FROM python:3.5

RUN pip install --no-cache-dir gunicorn psycopg2

# Install BDSS
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

CMD ["gunicorn", "app:app", "-b", "app"]
