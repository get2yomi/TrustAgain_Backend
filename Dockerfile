# Base Image
FROM python:3.12


# Create the app directory
RUN mkdir /app

# Set the working directory inside the container
WORKDIR /app

# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN pip install --upgrade pip 

# Copy requirements.txt and install dependencies
#COPY requirements.txt .
COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
#COPY . .
COPY . /app/

# Expose the port Django runs on
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

