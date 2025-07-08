# 📦 Installation Guide for City Population App

This guide shows how to deploy the City Population app and Elasticsearch into a Kubernetes cluster.

---

## 🧱 Prerequisites

- Docker
- Kubernetes cluster (Minikube, Kind, EKS, etc.)
- kubectl
- Helm 3.x
- Docker Hub account (for image push, if needed)

---

bash
## 1️⃣ Build & Push Docker Image (Optional)

If you haven't pushed your own image yet:
docker build -t your-dockerhub-user/city-population:latest ./app
docker push your-dockerhub-user/city-population:latest


2️⃣ Deploy Elasticsearch (Manual, No Auth)
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

3️⃣ Add the Helm Repo for City Population App
```bash
helm repo add city-population https://bahram663.github.io/city-population/charts
helm repo update
helm search repo city-population
```
4️⃣ Install the App via Helm

```bash
helm install city-app city-population/city-population \
  --namespace city-system \
  --create-namespace \
  --set image.repository=your-dockerhub-user/city-population \
  --set image.tag=latest \
  --set elasticsearch.host=elasticsearch.elastic-system.svc.cluster.local
```
Replace your-dockerhub-user if using a custom Docker image.

5️⃣ Access the API
Port forward the app to your local machine:



kubectl port-forward svc/city-app 8000:80 -n city-system
6️⃣ Test the API

Health:

```bash
curl http://localhost:8000/health
```

Add/update city:


```bash
curl -X POST http://localhost:8000/cities \
  -H "Content-Type: application/json" \
  -d '{"name": "Baku", "population": 2300000}'
```
Get population:


```bash
curl http://localhost:8000/cities/Baku
```
