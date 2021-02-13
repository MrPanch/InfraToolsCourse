FROM python:3

ARG DATA_DIR
ARG DB_NAME
ARG DB_HOST
ARG DB_PORT

ENV DATA_DIR ${DATA_DIR}
ENV DB_NAME ${DB_NAME}
ENV DB_HOST ${DB_HOST}
ENV DB_PORT ${DB_PORT}

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY fill-script.py ./

CMD python3 fill-script.py $DATA_DIR $DB_HOST $DB_PORT $DB_NAME
