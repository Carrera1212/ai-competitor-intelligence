# 1. Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /usr/src/app

# 3. Install the specific libraries needed
RUN pip install --no-cache-dir transformers torch

# 4. Copy the app.py file from your computer into the container
COPY app.py .

# 5. Run app.py when the container launches
CMD ["python", "app.py"]