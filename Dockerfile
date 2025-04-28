FROM python:3.12 as base


# This flag is important to output python logs correctly in docker!
ENV PYTHONUNBUFFERED 1
# Flag to optimize container size a bit by removing runtime python cache
ENV PYTHONDONTWRITEBYTECODE 1


COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "bot.py" ]