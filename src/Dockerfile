FROM python:3.9.18-alpine3.19
WORKDIR /app
COPY requirements.txt .
RUN apk upgrade
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONIOENCODING=utf8
COPY . .
EXPOSE 5000 8000
CMD ["python", "run.py"]