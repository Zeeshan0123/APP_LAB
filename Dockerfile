# Use official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy only the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the required application files
COPY utils.py APIs.py gradio_app.py /app/

# Expose necessary ports (FastAPI: 4100, Gradio: 7860)
EXPOSE 4100 7860

# Start FastAPI first, wait for it to be ready, then start Gradio
CMD uvicorn APIs:app --host 0.0.0.0 --port 4100 & \
    while ! nc -z localhost 4100; do sleep 1; done && \
    python gradio_app.py

