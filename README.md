# City Population App

This is a Python-based REST API for managing a list of cities and their populations. It uses **Elasticsearch** as a backend database and is fully containerized and ready for **Kubernetes** deployment using a **Helm chart**.

## 🔧 Features

- `/health` - Health check endpoint
- `/city` - Insert or update a city's population
- `/city/{name}` - Retrieve the population of a city
- Elasticsearch as a backend database
- Dockerized and packaged for Kubernetes via Helm

## 🚀 Tech Stack

- Python (FastAPI)
- Elasticsearch
- Docker
- Kubernetes
- Helm

## 📦 Deployment

The application can be deployed to any Kubernetes cluster. You can deploy it along with an Elasticsearch instance using Helm charts.

For step-by-step installation, see [`docs/INSTALL.md`](docs/INSTALL.md)

## 🐳 Docker

To build the Docker image manually:

```bash
git clone https://github.com/bahram663/city-population.git
cd city-population
docker build -t your-dockerhub-user/city-population:latest ./app
docker push your-dockerhub-user/city-population:latest
