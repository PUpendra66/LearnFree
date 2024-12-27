FROM python:3.12-slim

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y libmysqlclient-dev gcc pkg-config

# Set working directory
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port used by your application
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "coursespage.wsgi:application"]
