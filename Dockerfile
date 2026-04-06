# Start from a small Python base image.
FROM python:3.11-slim

# Use /app as the working directory inside the container.
WORKDIR /app

# Copy dependency list first so Docker can cache the install step.
COPY requirements.txt .

# Install Python dependencies needed for the project.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container.
COPY . .

# Run the sequential intro script when the container starts.
CMD ["python3", "ray_core_intro_example/02_ray_tasks_basic.py"]
