# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app file into the container
COPY whatsapp_sender.py .

# Expose the port that Streamlit listens on (default is 8501)
EXPOSE 8501

# Command to run the Streamlit app when the container starts
CMD ["streamlit", "run", "whatsapp_sender.py", "--server.port=8501"]
