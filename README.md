# learn_ray_data_concepts

Beginner-friendly exercises for learning Ray in a small Python project.

## What this project does

This repo is a lightweight sandbox for learning distributed computing concepts with Ray.

Right now the project explores three versions of the same basic lookup workflow:

- normal sequential Python
- Ray tasks executed with `@ray.remote`
- Ray tasks that read the fake database through Ray's object store with `ray.put()`

The example uses a tiny fake database of words plus a short artificial delay, so it is easier to see why parallel execution can finish faster.

The scripts also print database reference details so you can see which process is using which copy of the data.

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
docker run --rm --shm-size=3.19g learn-ray-data
```

If you want to give Ray more shared memory inside Docker and avoid `/dev/shm`
limits, use:

```bash
docker run --rm --shm-size=3.19g learn-ray-data
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

Run the object store example:

```bash
python3 ray_core_intro_example/03_object_store.py
```

Build the Docker image:

```bash
docker build -t learn-ray-data .
```

Run the Docker container with the Dockerfile default command:

```bash
docker run --rm --shm-size=3.19g learn-ray-data
```

Run the sequential example in Docker:

```bash
docker run --rm --shm-size=3.19g --entrypoint python3 learn-ray-data ray_core_intro_example/01_python_sequential.py
```

Run the basic Ray task example in Docker:

```bash
docker run --rm --shm-size=3.19g --entrypoint python3 learn-ray-data ray_core_intro_example/02_ray_tasks_basic.py
```

Run the object store example in Docker:

```bash
docker run --rm --shm-size=3.19g --entrypoint python3 learn-ray-data ray_core_intro_example/03_object_store.py
```

Clean up unused Docker images:

```bash
docker image prune
```

## Configuration

There are currently no project-specific environment variables required to run the examples.

The setup is intentionally simple:

- `requirements.txt` defines the Python dependency
- the `Dockerfile` defines the container environment and default example command

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
python3 ray_core_intro_example/02_ray_tasks_basic.py
```

That means the basic Ray task example is the current default container entry point.

### `main.py`

Contains a minimal `hello world` placeholder. It is not the main script for the current learning exercises.

### `ray_core_intro_example/00_shared.py`

Holds the shared helper logic used by the intro scripts:

- a fake in-memory database
- `retrieve()`, which simulates work with `time.sleep()`
- `describe_database()`, which formats process-level database identity information
- `print_database_references()`, which prints the database reference summary for each example
- `print_runtime()`, which prints elapsed runtime and results

This file exists so both example programs can reuse the same behavior and stay easy to compare.

### `ray_core_intro_example/01_python_sequential.py`

Runs the database lookups one by one using normal Python.

This script is useful because it provides the baseline behavior before introducing Ray and shows a single process-level database reference.

### `ray_core_intro_example/02_ray_tasks_basic.py`

Runs the same lookups as Ray tasks, then collects the results with `ray.get()`.

This script shows the smallest useful step from plain Python to distributed task execution in Ray and demonstrates that workers use their own module-level copies of the fake database.

### `ray_core_intro_example/03_object_store.py`

Runs the lookup tasks by first placing the fake database into Ray's object store with `ray.put()`, then passing the resulting object reference into each task.

This script highlights the difference between:

- the driver's original Python database
- the driver's `ObjectRef`
- the value returned by `ray.get(db_object_ref)` on the driver
- the object-store-backed database values materialized inside worker processes

### `useful_commands.txt`

Stores a few Docker commands for quick reference:

- build the image
- run the container
- prune unused images

## What to expect

- The sequential version should take longer because each lookup waits its turn.
- The Ray version should usually finish faster because multiple lookups can run concurrently.
- The object store version should also finish quickly and makes it clearer how data is shared in a real Ray cluster.
- In `03_object_store.py`, the driver still has its own Python database, and `ray.put()` creates a separate object-store copy referenced by `db_object_ref`.

## Current state

The project is still intentionally small, but it already provides:

- a reproducible environment
- a plain Python baseline
- a first Ray task example
- an object store example
- simple process-level diagnostics for seeing where each database reference lives

That makes it a good place to keep adding more Ray learning examples over time.
