FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
COPY ./API /app
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "85"]