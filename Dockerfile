FROM python

RUN pip install flask mongoengine flask_cors python-dotenv

WORKDIR /app

COPY . /app

CMD python app.py