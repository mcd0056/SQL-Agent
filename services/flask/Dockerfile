# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set environment variables
ENV OPENAI_API_KEY=
ENV MYSQL_HOST=
ENV MYSQL_ROOT_PASSWORD=
ENV MYSQL_USER=
ENV MYSQL_PASSWORD=
ENV MYSQL_DB=
ENV NAME World

# Run the app using Gunicorn. Replace 'main:app' with your Flask app's module and variable name.
CMD ["gunicorn", "-w", "4", "main:app", "--bind", "0.0.0.0:8000"]
