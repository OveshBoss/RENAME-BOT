# Base image
FROM python:3.10-slim

# Set timezone and sync system clock
ENV TZ=Asia/Kolkata
RUN apt-get update && \
    apt-get install -y tzdata ntpdate && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    ntpdate pool.ntp.org && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY main.py .

# Expose port (optional)
EXPOSE 8000

# Start the bot
CMD ["python", "main.py"]
