FROM python:3.11.6
COPY . ./
COPY ./requirements.txt /src/requirements.txt
ENV PORT 8000
ENV APP_HOME /src
WORKDIR $APP_HOME
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn main:app --host 0.0.0.0 --port $PORT