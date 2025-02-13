from kubernetes import client, config
from fastapi import FastAPI
import requests
import time
import os
import threading

# Load Kubernetes config
try:
    config.load_incluster_config()
except:
    config.load_kube_config()

# Define Kubernetes API clients
v1 = client.CoreV1Api()

# Loki Configuration
LOKI_URL = "http://loki:3100/loki/api/v1/push" 
 # Ensure Loki is running inside Docker

# FastAPI App
app = FastAPI()

def send_logs_to_loki(pod_name, namespace, log_data):
    """Send logs to Loki"""
    log_payload = {
        "streams": [
            {
                "stream": {"pod": pod_name, "namespace": namespace},
                "values": [[str(int(time.time() * 1e9)), log_data]]
            }
        ]
    }
    try:
        requests.post(LOKI_URL, json=log_payload)
    except Exception as e:
        print(f"⚠️ Failed to send logs to Loki: {e}")

def continuously_fetch_logs():
    """Continuously fetch logs from Kubernetes and send them to Loki"""
    namespace = "default"
    while True:
        pods = v1.list_namespaced_pod(namespace=namespace).items
        for pod in pods:
            pod_name = pod.metadata.name
            try:
                log_output = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace)
                send_logs_to_loki(pod_name, namespace, log_output)
            except Exception as e:
                print(f"⚠️ Could not fetch logs for {pod_name}: {e}")
        time.sleep(10)  # Fetch logs every 10 seconds

@app.get("/logs")
def fetch_logs():
    """Fetch logs from Kubernetes and return them"""
    namespace = "default"
    pods = v1.list_namespaced_pod(namespace=namespace).items
    all_logs = {}
    
    for pod in pods:
        pod_name = pod.metadata.name
        try:
            log_output = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace)
            all_logs[pod_name] = log_output
        except Exception as e:
            all_logs[pod_name] = f"⚠️ Could not fetch logs: {e}"
    
    return all_logs

if __name__ == "__main__":
    threading.Thread(target=continuously_fetch_logs, daemon=True).start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
