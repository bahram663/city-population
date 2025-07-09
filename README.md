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

## 🐳 Docker (optional)

To build the Docker image manually:

```bash
git clone https://github.com/bahram663/city-population.git
cd city-population
docker build -t your-dockerhub-user/city-population:latest ./app
docker push your-dockerhub-user/city-population:latest
```


# 📦 Installation Guide for City Population App

This guide shows how to deploy the City Population app and Elasticsearch into a Kubernetes cluster.

---

## 🧱 Prerequisites

- Docker
- Kubernetes cluster (Minikube, Kind, EKS, Microk8s etc.)
- kubectl
- Helm 3.x
- Ingress (optional)
- Docker Hub account (for image push, if needed)

---




## 1️⃣ Deploy Elasticsearch (Manual, No Auth)
We’ll create Elasticsearch using kubectl in a separate namespace:


---
```bash
kubectl create namespace elastic-system

kubectl create deployment elasticsearch \
  --image=docker.elastic.co/elasticsearch/elasticsearch:8.13.4 \
  -n elastic-system

kubectl set env deployment/elasticsearch \
  discovery.type=single-node \
  xpack.security.enabled=false \
  -n elastic-system

kubectl expose deployment elasticsearch \
  --port=9200 --target-port=9200 \
  -n elastic-system
```
Wait until the pod is ready:
```bash
kubectl get pods -n elastic-system -w
```

2️⃣ Add the Helm Repo for City Population App
```bash
helm repo add city-population https://bahram663.github.io/city-population/charts
helm repo update
helm search repo city-population
```
3️⃣ Install the App via Helm

```bash
helm install city-api city-population/city-api \
  --namespace city-population \
  --create-namespace \
  --set elasticsearch.host=http://elasticsearch.elastic-system.svc.cluster.local:9200
```
You can use your-dockerhub-user if using a custom Docker image.

4️⃣ Access the API
Port forward the app to your local machine


```bash
kubectl port-forward svc/city-api 8000:80 -n city-population
```
5️⃣ Test the API

Health:

```bash
curl http://localhost:8000/health
```

Add/update city:


```bash
curl -X POST http://localhost:8000/city \
  -H "Content-Type: application/json" \
  -d '{"name": "Baku", "population": 2300000}'
```
Get population:


```bash
curl http://localhost:8000/city/Baku
```
