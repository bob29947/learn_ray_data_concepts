# learn_ray_data_concepts

Beginner-friendly exercises for learning Ray in a small Python project.

## What this project does

This repo is a lightweight sandbox for learning distributed computing concepts with Ray.

Right now the main example compares two ways of doing the same work:

- normal sequential Python
- Ray tasks executed with `@ray.remote`

The example uses a tiny fake database of words plus a short artificial delay, so it is easier to see why parallel execution can finish faster.

## Technologies used

- Python 3.11
- Ray with the `ray[data]` extra
- Docker for repeatable local runs

## Setup

### Local Python setup

Create and activate a virtual environment if you want an isolated local setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Why this helps:

- the virtual environment keeps project dependencies separate from your system Python
- `requirements.txt` installs Ray so the example scripts can run

### Docker setup

If you prefer not to manage Python locally, you can use Docker instead:

```bash
docker build -t learn-ray-data .
docker run --rm learn-ray-data
```

Why Docker is useful here:

- it gives the project a repeatable runtime environment
- it avoids redoing setup steps later

## Commands

Run the sequential Python example:

```bash
python3 ray_core_intro_example/01_python_sequential.py
```

Run the Ray task example:

```bash
python3 ray_core_intro_example/02_ray_tasks_basic.py
```

Build the Docker image:

```bash
docker build -t learn-ray-data .
```

Run the Docker container:

```bash
docker run --rm learn-ray-data
```

Clean up unused Docker images:

```bash
docker image prune
```

## Configuration

There are currently no project-specific environment variables required to run the examples.

The setup is intentionally simple:

- `requirements.txt` defines the Python dependency
- the `Dockerfile` defines the container environment

## Project structure

### `requirements.txt`

Installs:

```txt
ray[data]
```

This prepares the project for Ray experiments now and Ray Data experiments later.

### `Dockerfile`

Builds a Python 3.11 container, installs dependencies, copies the repo into `/app`, and currently runs:

```bash
python3 ray_core_intro_example/01_python_sequential.py
```

That means the sequential intro example is the current default container entry point.

### `main.py`

Contains a minimal `hello world` placeholder. It is not the main script for the current learning exercises.

### `ray_core_intro_example/00_shared.py`

Holds the shared helper logic used by the intro scripts:

- a fake in-memory database
- `retrieve()`, which simulates work with `time.sleep()`
- `print_runtime()`, which prints elapsed runtime and results

This file exists so both example programs can reuse the same behavior and stay easy to compare.

### `ray_core_intro_example/01_python_sequential.py`

Runs the database lookups one by one using normal Python.

This script is useful because it provides the baseline behavior before introducing Ray.

### `ray_core_intro_example/02_ray_tasks_basic.py`

Runs the same lookups as Ray tasks, then collects the results with `ray.get()`.

This script shows the smallest useful step from plain Python to distributed task execution in Ray.

### `useful_commands.txt`

Stores a few Docker commands for quick reference:

- build the image
- run the container
- prune unused images

## What to expect

- The sequential version should take longer because each lookup waits its turn.
- The Ray version should usually finish faster because multiple lookups can run concurrently.

## Current state

The project is still intentionally small, but it already provides:

- a reproducible environment
- a plain Python baseline
- a first Ray task example

That makes it a good place to keep adding more Ray learning examples over time.
