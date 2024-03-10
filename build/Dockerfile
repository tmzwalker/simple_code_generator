# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY src/ .

# Check if the OPENAI_API_KEY environment variable exists
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Expose the port on which the FastAPI application will run (default is 8000)
EXPOSE 8000

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]