FROM arm64v8/python:3.9-buster
RUN pip install --upgrade pip

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8060
ENV IS_CONTAINER=True


CMD ["python3", "./index.py"]