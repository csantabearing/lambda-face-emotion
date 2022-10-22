# Deployment on ECS

## Update images to ECR

Authenticate docker:

```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 681261969843.dkr.ecr.us-east-1.amazonaws.com
```

We need to do the following steps for each of the docker images:

- Create a repo
- Build the image
- Tag the image
- Push the image to the repo

The repositories can be created on the console: <https://github.com/csantabearing/lambda-face-emotion/tree/triton>  or through aws cli:

```
aws ecr create-repository --repository-name yourname/reponame
```

Build the image with docker

```
docker build -t yourname/reponame .
```

Tagging the images

```
docker tag yourname/reponame:latest 681261969843.dkr.ecr.us-east-1.amazonaws.com/yourname/reponame:latest
```

Push the images

```
docker push 681261969843.dkr.ecr.us-east-1.amazonaws.com/yourname/reponame:latest
```

Repeat these steps for all the docker images.

## ECS Cluster

Create a new Networking only ECS cluster from the console <https://us-east-1.console.aws.amazon.com/ecs/home?region=us-east-1#/clusters> or cli:

```
aws ecs create-cluster --cluster-name yourname-cluster
```

Define tasks for each of the docker images (main, face-emotion, pet-bokeh, triton) in the console <https://us-east-1.console.aws.amazon.com/ecs/home?region=us-east-1#/taskDefinitions/create>:

- Select fargate launch type
- Change the name of the task: (yourname-main, yourname-face-emotion, yourname-pet-bokeh)
- Change the task memory and CPU
- Add container:
  - Change the name
  - Use the image URI (e.g `681261969843.dkr.ecr.us-east-1.amazonaws.com/mlo4/face-emotion:latest`)
  - Add 8000 to the port mappings
  - For triton change the command to (`tritonserver --model-repository=s3://triton-repository/models/`)
- Create

Inside your cluster, create a new service for each task (yourname-main, yourname-face-emotion, yourname-pet-bokeh, yourname-triton):

- Launch type: Fargate
- Pick the Task definition: (yourname-main, yourname-face-emotion, yourname-pet-bokeh, yourname-triton)
- Service name: (main, face-emotion, pet-bokeh)
- Number of tasks: 1
- Next page
- Cluster VPC: Default
- Subnets: Pick one
- Edit security group
  - Custom TCP port 8000
- Auto-assign public IP: Enabled
- Enable service discovery integration: True
  - Namespace name: local
  - Service discovery name: (main, face-emotion, pet-bokeh, triton)
  - TTL: 60 seconds
- Create service

To update a service if the docker changed run `aws ecs update-service --cluster mlo4test --service face-emotion --force-new-deployment` or update from the console with "Force New Deployment"

Check <http://main.tasks.public.ip:8000/docs>
