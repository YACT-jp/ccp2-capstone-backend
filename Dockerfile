FROM python:3

WORKDIR /usr/src/app
RUN pip install flask
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]