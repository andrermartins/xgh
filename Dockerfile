FROM python:2.7
RUN mkdir -p /app/
COPY . /app/
RUN pip install --upgrade pip
RUN pip install -i https://pypi.python.org/simple stomp.py
RUN pip install python-logstash
RUN pip install logstash_formatter
RUN pip install logstash_handler
RUN pip install psycopg2
RUN pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose

WORKDIR /app/
ENTRYPOINT ["python","init.py"]
