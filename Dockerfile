FROM python:3.10.2 as django
ENV PYTHONBUFFERED=1

WORKDIR /appevent
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -Ur requirements.txt

WORKDIR /appevent/backend
COPY ./backend .

EXPOSE 8000
