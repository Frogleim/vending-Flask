FROM python:3.9

WORKDIR /backend

# Copy just the requirements file first to leverage Docker caching
COPY requirements.txt .

RUN apt-get update && apt-get install -y xdotool && apt-get install -y firefox-esr

# Install dependencies
RUN pip install --upgrade pip==21.2.4 && \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 5000

# Command to run the application
CMD ["python", "main.py"]

