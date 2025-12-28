FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn

COPY apps/interface /app/apps/interface

EXPOSE 3000

CMD ["uvicorn", "apps.interface.server:app", "--host", "0.0.0.0", "--port", "3000"]