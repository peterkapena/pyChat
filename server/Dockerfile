# Use a base Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install git to clone the repository
RUN apt-get update && apt-get install -y git

# Clone the code from the repository
RUN git clone https://github.com/peterkapena/pyChat/app

# Install dependencies
# RUN pip install -r requirements.txt

EXPOSE 12000

# Set the command to run when the container starts
CMD ["python", "server/index.py"]
## Useful commands
#docker build -t py_chat_server .
#docker run -d -p 12000:12000 kapenapeter/py_chat_server 
#docker ps