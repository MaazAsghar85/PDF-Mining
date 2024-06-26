# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# If your Python script has dependencies, you can list them in a requirements.txt file
RUN pip install --no-cache-dir PyMuPDF

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD python Pdf-Tree.py && python Extraction.py