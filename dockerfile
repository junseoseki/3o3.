FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["pytest", "--alluredir=allure-results"]
