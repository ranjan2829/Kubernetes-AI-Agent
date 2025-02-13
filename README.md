# Kubernetes AI Agent

## Overview
Kubernetes AI Agent is an intelligent system designed to analyze Kubernetes logs for anomalies, failures, and performance issues. It uses AI-driven insights to help DevOps teams monitor and optimize Kubernetes-based deployments.

## Features
- **AI-Powered Log Analysis**: Uses deep learning models to detect anomalies in Kubernetes logs.
- **Real-time Monitoring**: Continuously monitors logs and provides structured insights.
- **Automated CLI Commands**: Suggests optimal CLI commands for debugging.
- **Scalability**: Includes Kubernetes Horizontal Pod Autoscaler (HPA) for auto-scaling deployments.
- **FastAPI Integration**: Provides a REST API interface to interact with the AI agent.
- **Deployment-ready**: Comes with Kubernetes YAML configurations for easy deployment.

---

## Tech Stack
- **Backend**: FastAPI (Python)
- **AI Model**: Groq DeepSeek-R1-Distill-Qwen-32B
- **Orchestration**: Kubernetes
- **Infrastructure**: Docker, Kubernetes, Horizontal Pod Autoscaler (HPA)
- **Monitoring & Logging**: Fluentd
- **Storage**: Local file system for logs
- **Configuration Management**: dotenv for environment variables

---

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.10+
- Docker
- Kubernetes (kubectl, minikube, or cloud provider cluster)
- Helm (for Fluentd setup if required)
- Virtual Environment (optional but recommended)

### Setup Instructions
```sh
# Clone the repository
git clone https://github.com/your-repo/Kubernetes-AI-Agent.git
cd Kubernetes-AI-Agent

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
nano .env  # Add your GROQ_API_KEY
```

---

## Usage
### Running Locally
```sh
python kube_agent.py
```

### Running with FastAPI
```sh
uvicorn api:app --host 0.0.0.0 --port 8080
```

### Kubernetes Deployment
```sh
# Apply Deployment and Service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Verify Deployment
kubectl get pods
kubectl get services
```

### Enable Auto-Scaling
```sh
kubectl apply -f hpa.yaml
kubectl get hpa
```

---

## Kubernetes Deployment YAML Files
### Deployment File (`deployment.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp-container
        image: myapp-image:latest
        ports:
        - containerPort: 80
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Service File (`service.yaml`)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

### Horizontal Pod Autoscaler (`hpa.yaml`)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

---

## API Endpoints
| Method | Endpoint      | Description                        |
|--------|--------------|------------------------------------|
| GET    | `/`          | Health check                      |
| POST   | `/analyze`   | Analyze Kubernetes logs           |

---

## Example Logs and Analysis
### Input Logs (Example `app_logs.txt`)
```
INFO: 10.244.0.1 - "GET / HTTP/1.1" 200 OK
ERROR: Failed to pull image "myapp-container"
```

### AI-Generated Output (`analysis_output.txt`)
```
| Log Entry | Severity | Suggested Fix |
|-----------|---------|---------------|
| Failed to pull image | ERROR | Ensure the image exists in the registry |
```

---

## Contributors
- **Your Name** ([@yourGitHub](https://github.com/yourGitHub))

## License
This project is licensed under the MIT License.

## Future Improvements
- Add support for multi-cloud Kubernetes clusters.
- Enhance AI model to include predictive failure analysis.
- Integrate with Prometheus and Grafana for better visualization.

