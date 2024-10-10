from kubernetes import client, config
from prometheus_client import start_http_server, Counter
import time
import numpy as np
from sklearn.linear_model import LinearRegression
import os

# Initialize Kubernetes configuration
try:
    config.load_incluster_config()
except config.ConfigException:
    config.load_kube_config()

apps_v1 = client.AppsV1Api()

# Constants
NAMESPACE = os.getenv('NAMESPACE', 'default')
DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME', 'example-deployment')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '60'))
PREDICTION_WINDOW = int(os.getenv('PREDICTION_WINDOW', '5'))
SCALE_THRESHOLD = float(os.getenv('SCALE_THRESHOLD', '0.6'))
MIN_PODS = int(os.getenv('MIN_PODS', '2'))
MAX_PODS = int(os.getenv('MAX_PODS', '15'))
SCALE_INCREMENT = int(os.getenv('SCALE_INCREMENT', '5'))

# Simulated metric for user count
user_count = Counter('user_count', 'Number of active users')

def get_current_user_count():
    # Simulating increasing user count for demonstration
    current_value = user_count._value.get()
    user_count.inc(np.random.randint(1, 10))
    return float(current_value)

def predict_trend(historical_data):
    if len(historical_data) < PREDICTION_WINDOW:
        return 0
    
    X = np.array(range(len(historical_data))).reshape(-1, 1)
    y = np.array(historical_data)
    
    model = LinearRegression()
    model.fit(X, y)
    
    return model.coef_[0]

def scale_deployment(trend):
    try:
        deployment = apps_v1.read_namespaced_deployment(
            name=DEPLOYMENT_NAME,
            namespace=NAMESPACE
        )
        
        current_replicas = deployment.spec.replicas
        
        if trend > SCALE_THRESHOLD and current_replicas < MAX_PODS:
            new_replicas = min(current_replicas + SCALE_INCREMENT, MAX_PODS)
        elif trend < -SCALE_THRESHOLD and current_replicas > MIN_PODS:
            new_replicas = max(current_replicas - SCALE_INCREMENT, MIN_PODS)
        else:
            return
        
        deployment.spec.replicas = new_replicas
        
        apps_v1.patch_namespaced_deployment(
            name=DEPLOYMENT_NAME,
            namespace=NAMESPACE,
            body=deployment
        )
        
        print(f"Scaled deployment from {current_replicas} to {new_replicas} pods")
    
    except Exception as e:
        print(f"Error scaling deployment: {e}")

def main():
    print(f"Starting custom scaler for deployment {DEPLOYMENT_NAME} in namespace {NAMESPACE}")
    start_http_server(8000)
    historical_data = []
    
    while True:
        current_users = get_current_user_count()
        historical_data.append(current_users)
        
        if len(historical_data) > PREDICTION_WINDOW:
            historical_data.pop(0)
        
        trend = predict_trend(historical_data)
        print(f"Current users: {current_users}, Current trend: {trend}")
        
        scale_deployment(trend)
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
