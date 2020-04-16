FROM python:3.6-alpine

ENV STUDENT_ID 2019000000
ENV STUDENT_PASSWORD 123456

COPY src/check_in.py src/
COPY src/form.py src/
COPY main.py main.py
COPY requirements.txt requirements.txt

RUN echo "https://mirrors.ustc.edu.cn/alpine/v3.11/main/" > /etc/apk/repositories \
    && apk add --no-cache --virtual BUILD gcc musl-dev \
    && apk add tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del BUILD

CMD [ "python", "main.py" ]
