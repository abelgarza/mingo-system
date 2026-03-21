# This is a foundational Dockerfile draft, created to demonstrate 
# how your new initialization process makes Dockerizing trivial.
# We map your Ubuntu environment with Python and Node.js to a container.

FROM ubuntu:24.04

# Avoid tzdata interactive prompt during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Install base system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up the workspace directory
WORKDIR /opt/mingo-system

# Copy the entire clean source code into the container
# (.dockerignore ensures .env and .venvs are NOT copied)
COPY . .

# Run the idempotent bootstrap script
# This automatically spins up the python virtual environment, 
# installs the python dependencies, and runs npm install for the CLI.
RUN chmod +x scripts/bootstrap.sh && ./scripts/bootstrap.sh

# The container is now fully "planchado". 
# When mingo-system is ready for production, change this CMD to start the orchestrator directly!
CMD ["bash", "-c", "source scripts/mingo-env.sh && bash"]
