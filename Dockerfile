FROM python

RUN pip install kafka-python snowplow_analytics_sdk pydblite

COPY consumer.py /root/consumer.py

ENV PYTHONUNBUFFERED=1

CMD [ "python", "/root/consumer.py" ]

# FROM python

# WORKDIR /root/sample

# COPY schemas/ /root/sample/schemas

# CMD [ "python", "-m", "http.server", "7000"]
