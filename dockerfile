FROM mcr.microsoft.com/playwright/python:v1.57.0-2

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["pytest", "--alluredir=allure-results"]
