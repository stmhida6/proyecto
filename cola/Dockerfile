
FROM python:3.9-slim
WORKDIR /app
COPY consumidor.py .
RUN pip install pika mysql-connector-python
#EXPOSE 5000
# Run app.py when the container launches
CMD ["python","-u","app.py"]