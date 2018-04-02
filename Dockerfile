FROM python:3.6
COPY . /app/
WORKDIR /app/
RUN pip3 install -U pip \
    && pip3 install -r requirements.txt
WORKDIR /app/api
RUN apistar create_tables
CMD ["apistar", "run", "--host", "0.0.0.0", "--port", "8080"]
