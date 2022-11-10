# Kubeflow

## Create MiniKF Instance

- Go to: <https://aws.amazon.com/marketplace/pp/prodview-7shm7yqkubjhg>
- Accept the terms
- Launch an instance using the EC2 console
- Make sure to enable public ip
- Open ports 22, 80, 443, 8443, 32123
- ssh into the machine and run minikf to see the progress
- Wait for it to finish and log into kubeflow in the address and the credentials provided
![Credengials](/images/creds.png)
- Create a new volume called `models`
- Create a notebook instance
- Open a terminal in the notebook instance and clone the repo
- Install requirements
- Open the training notebook Training.ipynb
- Train and save the model on the `models` volume
- ssh back into the machine and deploy the model

```
kubectl apply -f K8s/
```

- Check the model with the Inference.ipynb notebook
