FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["streamlit", "run", "app.py"]
