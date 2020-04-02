FROM python

RUN pip install flask mongoengine flask_cors

WORKDIR /app

COPY . /app

CMD python app.py