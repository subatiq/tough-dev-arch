FROM python:3.10.7-slim


WORKDIR /app
COPY Pipfile Pipfile.lock ./

RUN  pip install pipenv && pipenv install --deploy --system && pip uninstall pipenv -y

COPY src src/

EXPOSE 5000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "5000"]

