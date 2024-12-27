# Use a slim Python image as the base
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y libmysqlclient-dev gcc pkg-config

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 8000

# Command to run your application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "coursespage.wsgi:application"]
