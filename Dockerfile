# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

# Upgrade pip as root
RUN python3 -m pip install --upgrade pip

# Create user
RUN useradd --create-home --shell /bin/bash app_user

# Use user
USER app_user

# Go to home folder
WORKDIR /home/app_user

# Create app folder
RUN mkdir app_name

# Go to app folder
WORKDIR /home/app_user/app_name

# Copy all app files (except .dockerignore)
COPY . .

# Define which command line processor to use
CMD ["bash"]

# Copy requirements file
COPY requirements.txt ./

# Add local/bin to PATH
ENV PATH="/home/app_user/.local/bin:${PATH}"

# Install virtual environment
RUN python3 -m pip install --user virtualenv

# Creates virtual environment
RUN python3 -m venv venv

# Starts virtual environment
RUN  /bin/bash -c "source venv/bin/activate"

# Install app dependencies
RUN pip install --no-cache-dir -c requirements.txt django-currentuser

# Open TCP port
EXPOSE 8000

WORKDIR /home/app_user/app_name
CMD [ "source", "venv/bin/activate"]
CMD [ "python3", "manage.py" , "runserver", "run", "0.0.0.0:8000"]
