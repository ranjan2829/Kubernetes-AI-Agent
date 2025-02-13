import os
from dotenv import load_dotenv  # type: ignore

from phi.agent import Agent  # type: ignore
from phi.model.groq import Groq  # type: ignore

load_dotenv()

# Read logs from file
def read_logs(file_path="system_logs.txt"):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "Log file not found."

# Define Kubernetes AI Agent
kubernetes_ai_agent = Agent(
    name="Kubernetes Log Analyzer",
    role="Analyze Kubernetes system logs for anomalies and failures.",
    model=Groq(id="deepseek-r1-distill-qwen-32b", api_key=os.getenv("GROQ_API_KEY")),
    instructions=[
        "Analyze the latest Kubernetes logs.",
        "Detect any anomalies, failures, or warnings.",
        "Provide insights in a structured table format."
    ],
    show_tool_calls=True,
    markdown=True,
)

# Read logs and analyze
logs = read_logs()
kubernetes_ai_agent.print_response(f"Analyze the following Kubernetes logs and report any anomalies:\n{logs}", stream=True)