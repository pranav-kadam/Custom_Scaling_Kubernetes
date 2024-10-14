### Start minikube
`minikube start`
### Build the Docker image
```docker build -t custom-k8s-scaler:latest . ```

### Load the image into Minikube
```minikube image load custom-k8s-scaler:latest ```

### Apply the Kubernetes manifests
```kubectl apply -f k8s-manifests.yaml```

### Verify the deployments
```kubectl get deployments```

### Monitor the scaler
```kubectl logs -f deployment/custom-scaler```

### To test the scaling:
 - The example deployment starts with 2 replicas
 - The custom scaler will simulate increasing user traffic
 - When the trend exceeds the threshold, it will scale up the example-deployment by 5 pods

### Clean up
```kubectl delete -f k8s-manifests.yaml```
```minikube stop ```
