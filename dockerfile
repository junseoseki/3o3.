FROM mcr.microsoft.com/playwright/python:v1.57.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y fonts-nanum locales
RUN locale-gen ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

COPY . .

CMD ["pytest", "-s", "--alluredir=/app/allure-results", "--browser", "chromium", "--browser", "firefox", "--browser", "webkit"]
