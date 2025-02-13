import time
import re
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

APP_LOG_FILE = "app_logs.txt"
SYSTEM_LOG_FILE = "system_logs.txt"

# Function to get only the most recent log line
def get_latest_log(log_text):
    lines = log_text.strip().split("\n")
    return lines[-1] if lines else "⚠️ No logs available"

# Function to fetch and store only the most recent log per pod
def fetch_and_store_logs():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store application logs (overwrite with latest logs)
    with open(APP_LOG_FILE, "w") as app_log:
        app_log.write(f"===== Latest Application Logs @ {timestamp} =====\n\n")

        # Fetch Deployments
        app_log.write("✅ Deployments found:\n")
        deployments = apps_v1.list_namespaced_deployment(namespace="default")
        for deploy in deployments.items:
            app_log.write(f"📦 Deployment: {deploy.metadata.name}\n")

        # Fetch latest log for each application pod
        app_log.write("\n📜 Latest Application Logs (Namespace: default):\n")
        pods = v1.list_namespaced_pod(namespace="default")
        for pod in pods.items:
            app_log.write(f"\n📜 Latest Log for Pod {pod.metadata.name}:\n")
            try:
                log_output = v1.read_namespaced_pod_log(name=pod.metadata.name, namespace="default")
                latest_log = get_latest_log(log_output)  # Keep only the latest line
                app_log.write(latest_log + "\n")
            except Exception as e:
                app_log.write(f"⚠️ Could not fetch logs: {e}\n")

    # Store system logs separately (overwrite with latest logs)
    with open(SYSTEM_LOG_FILE, "w") as sys_log:
        sys_log.write(f"===== Latest System Logs @ {timestamp} =====\n\n")

        # Fetch latest log for each system pod
        sys_log.write("⚙️ Latest System Logs (Namespace: kube-system):\n")
        sys_pods = v1.list_namespaced_pod(namespace="kube-system")
        for pod in sys_pods.items:
            sys_log.write(f"\n⚙️ Latest Log for System Pod {pod.metadata.name}:\n")
            try:
                log_output = v1.read_namespaced_pod_log(name=pod.metadata.name, namespace="kube-system")
                latest_log = get_latest_log(log_output)  # Keep only the latest line
                sys_log.write(latest_log + "\n")
            except Exception as e:
                sys_log.write(f"⚠️ Could not fetch logs: {e}\n")

if __name__ == "__main__":
    print("Starting continuous Kubernetes log collection... Press Ctrl+C to stop.")
    while True:
        fetch_and_store_logs()
        print("✅ Logs updated. Sleeping for 10 seconds...")
        time.sleep(10)  # Fetch logs every 10 seconds
