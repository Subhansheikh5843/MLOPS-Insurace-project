# Use an official Python 3.10 image from Docker Hub
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Copy your application code
COPY . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 5000

# Command to run the FastAPI app
CMD ["python3", "app.py"]
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]


# ---------------------explanation-----------------
#   Base Image


# FROM python:3.10-slim-buster
# This line tells Docker to start with an official, lightweight version of Python 3.10 that is built on the "buster" version of Debian Linux. It provides a clean slate with Python already installed.

# Set the Working Directory

# WORKDIR /app
# This command sets the default directory inside the container to /app. All subsequent commands will operate in this folder.

# Copy Your Application Code

# COPY . /app
# This line copies everything (all your application files and folders) from the directory where the Dockerfile lives on your local machine into the /app directory inside the container.

# Install the Dependencies

# RUN pip install -r requirements.txt
# This step installs all the Python packages that your application needs. The requirements.txt file lists all these packages. Docker runs this command to make sure your app can use the needed libraries.

# Expose the Port


# EXPOSE 5000
# This command tells Docker that the container will listen on port 5000. This is important for the networking setup so that your app can receive traffic on that port (in this example, it’s used by FastAPI).

# Command to Run the App


# CMD ["python3", "app.py"]
# # CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
# The CMD instruction sets the default command to run when the container starts. Here, it tells Docker to run python3 app.py, which starts your FastAPI (or another Python) application. The second line is commented out (meaning it is not active), but it shows an alternative way to run a FastAPI app using uvicorn on port 8080.