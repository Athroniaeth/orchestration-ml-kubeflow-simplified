cd C:\Users\pierr\OneDrive\Bureau\Projet\kubeflow_simplifier

minikube stop
minikube delete
minikube start --driver=docker
kubectl delete --filename deployment.yaml
kubectl delete --filename services.yaml
kubectl create --filename deployment.yaml
kubectl create --filename services.yaml
minikube addons enable metrics-server
minikube dashboard
PAUSE