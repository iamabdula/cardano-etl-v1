# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory in the container
WORKDIR /app

# Install dependencies first (copy requirements.txt)
COPY requirements.txt /app/
COPY data/input_dataset_csv.csv /app/
COPY data/input_dataset_json.json /app/
COPY data/input_dataset_xml.xml /app/

# Install dependencies

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/
COPY data /app/data

# Expose any ports if necessary (for example, if you run a web UI)
# EXPOSE 8080

# Command to run your ETL process
CMD ["python", "src/main.py"]
