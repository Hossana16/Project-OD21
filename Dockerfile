# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    python3-gdal \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Install GDAL Python bindings
RUN pip install --upgrade pip
RUN pip install GDAL==$(gdal-config --version)

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run manage.py runserver when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
