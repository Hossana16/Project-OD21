# Use an official Python runtime as a parent image
FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV production

# Set working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt .
# RUN pip install --no-cache-dir -r /Project-OD21/requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
