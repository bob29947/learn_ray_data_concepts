# learn_ray_data_concepts

## April 1, 2026

Today I set up the starter foundation for this project so I can learn Ray Data without having to rebuild the environment from scratch later.

### What was added

#### `requirements.txt`

Added:

```txt
ray[data]
```

How it works:

This file tells Python which package to install for the project. In this case, it installs Ray with the Ray Data extras, so the environment is ready for Ray Data experiments when I start writing them.

#### `main.py`

Added:

```python
print("hello world")
```

How it works:

This is the current entry point for the project. Right now it is intentionally simple and only prints `hello world`. The purpose is to confirm that the project runs correctly and that the Docker setup is wired to the right file.

#### `Dockerfile`

Added a Docker setup for running the project in a repeatable container.

How it works:

- `FROM python:3.11-slim` starts from a lightweight Python image
- `WORKDIR /app` sets `/app` as the working directory inside the container
- `COPY requirements.txt .` copies the dependency file in first
- `RUN pip install --no-cache-dir -r requirements.txt` installs the project dependencies
- `COPY . .` copies the rest of the project files into the container
- `CMD ["python3", "main.py"]` makes the container run `main.py` when it starts

The main benefit is that I do not need to remember local environment setup details every time. Docker gives me a consistent way to run the project.

#### `useful_commands.txt`

Added notes for the Docker commands I will probably want later.

How it works:

It stores the basic commands for rebuilding and running the container:

```bash
docker build -t learn-ray-data .
docker run --rm learn-ray-data
```

- The build command creates the Docker image
- The run command starts a container from that image
- `--rm` removes the container after it finishes

#### `.gitignore`

Added ignore rules for local files that should not be committed.

How it works:

- `.DS_Store` is macOS metadata
- `__pycache__/` is Python bytecode cache output

This keeps the repo cleaner.

#### `.dockerignore`

Added ignore rules for files that should not be copied into the Docker build context.

How it works:

- `.git` is excluded so git history is not sent into the Docker build
- `__pycache__` and `*.pyc` are excluded because Python cache files are not needed in the image

This helps keep the build context smaller and avoids copying unnecessary files.

### Current state after today's work

The project is still very minimal, but the important setup is now in place:

- Ray Data is included as a dependency
- The project has a Python entry point
- The repo can be built and run with Docker
- The basic commands are written down for later reference

Right now the project does not contain Ray Data logic yet. Today was mainly about getting the environment and project structure ready so future work is easier to start.
