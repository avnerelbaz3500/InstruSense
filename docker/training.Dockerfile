FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install numpy scipy scikit-learn
CMD ["python", "apps/training/train_model.py"]
