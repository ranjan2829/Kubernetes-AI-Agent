import time
from datetime import datetime
from kubernetes import client, config

# Load Kubernetes config (inside cluster or locally)
try:
    config.load_incluster_config()
except:
    config.load_kube_config()

# Define Kubernetes API clients
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

LOG_FILE = "kube_logs.txt"

# Function to fetch and store logs
def fetch_and_store_logs():
    with open(LOG_FILE, "w") as f:  # Overwrites the old logs each run
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"===== Kubernetes Logs @ {timestamp} =====\n\n")

        # Fetch Deployments
        f.write("✅ Deployments found:\n")
        deployments = apps_v1.list_namespaced_deployment(namespace="default")
        for deploy in deployments.items:
            f.write(f"📦 Deployment: {deploy.metadata.name}\n")

        # Fetch Application Logs from "default" namespace
        f.write("\n📜 Application Logs (Namespace: default):\n")
        pods = v1.list_namespaced_pod(namespace="default")
        for pod in pods.items:
            f.write(f"\n📜 Logs for Pod {pod.metadata.name}:\n")
            try:
                log_output = v1.read_namespaced_pod_log(name=pod.metadata.name, namespace="default")
                f.write(log_output + "\n")
            except Exception as e:
                f.write(f"⚠️ Could not fetch logs: {e}\n")

        # Fetch System Logs from "kube-system" namespace
        f.write("\n⚙️ System Logs (Namespace: kube-system):\n")
        sys_pods = v1.list_namespaced_pod(namespace="kube-system")
        for pod in sys_pods.items:
            f.write(f"\n⚙️ Logs for System Pod {pod.metadata.name}:\n")
            try:
                log_output = v1.read_namespaced_pod_log(name=pod.metadata.name, namespace="kube-system")
                f.write(log_output + "\n")
            except Exception as e:
                f.write(f"⚠️ Could not fetch logs: {e}\n")

if __name__ == "__main__":
    print("Starting continuous Kubernetes log collection... Press Ctrl+C to stop.")
    while True:
        fetch_and_store_logs()
        print("✅ Logs updated. Sleeping for 10 seconds...")
        time.sleep(10)  # Fetch logs every 60 seconds
