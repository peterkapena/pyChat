# Use a base Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files to the working directory
COPY message.py /app/message.py
COPY index.py /app/index.py

EXPOSE 12000

# Set the command to run when the container starts
CMD ["python", "index.py"]

### Useful commands
#docker build -t py_chat_server .
#docker run -p 12000:12000 py_chat_server 
#docker ps
