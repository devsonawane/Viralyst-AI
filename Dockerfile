# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
# We add --no-cache-dir to reduce image size
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application's code into the container at /code
COPY . /code/

# Make port 8501 available to the world outside this container (Streamlit's default port)
EXPOSE 8501

# Define environment variable
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_HEADLESS=true

# Run streamlit_app.py when the container launches
# The --server.address=0.0.0.0 is important to make it accessible from outside the container
CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

