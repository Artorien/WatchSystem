FROM python:3.11

WORKDIR /main

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000"]
