# Use the official Python dev container image as a base
FROM mcr.microsoft.com/vscode/devcontainers/python:3.13

# Set the working directory inside the container
WORKDIR /workspaces/civic-voting-project

# Install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Install Google Cloud SDK
RUN echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && apt-get -y install apt-transport-https ca-certificates gnupg \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && apt-get update && apt-get -y install google-cloud-sdk \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
