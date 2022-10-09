# Deployment on EC2

## Create EC2 Instance

- Go to EC2 console: <https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1>
- Create EC2 instance
- Pick amazon linux
- Pick instance type: At least t3.medium
- Create key-pair
- Download key
- Edit network
- Enable IPV4 address
- Open ports 8000-8003 from anywhere
- Launch Instance

## Install dependencies

- Get the ip address of the instance
- Change key permissions to 400 (`chmod 400 key.pem`)
- SSH into the machine `ssh -i key.pem ec2-user@ec2.ip.address`
- Install git if needed (`sudo apt install git` for ubuntu based distros, `sudo yum install git` for amazon linux)
- Install Docker (`sudo apt install docker` for ubuntu based distros, `sudo yum install docker` for amazon linux)
- Start Docker (`sudo systemctl start docker`)
- Add user to docker group (`sudo usermod -aG docker ${USER}`)
- Logout and Login again through SSH to take the group changes into account
- Check if docker installed correctly (`docker run hello-world`)
- Install Docker-Compose

```
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version
```

# Model repositories

## Face-bokeh

- Rename `frozen_inference_graph.pb` to `model.graphdef`
- Write the config.pbtxt with:
  - platform: "tensorflow_graphdef"
  - The input tensor is called `ImageTensor` and should be UINT8 with dims `[-1,513,513,3]`
  - The output tensor is called `ResizeBilinear_3` and should be FP32 with dims `[-1,513,513,21]`
- Upload to s3 with the following folder strutcture

```bash
    models/
    └─face-bokeh/
      └─config.pbtxt
      └─1/
        └─model.graphdef
```

## Face-emotion

- Load the `model.h5` file and convert into the saved model format
- Write the config.pbtxt with:
  - platform: "tensorflow_savedmodel"
  - The input should be FP32 with dims `[-1,48,48,1]`
  - The output should be FP32 with dims `[-1,7]`
- Upload to s3 with the following strutcture

```bash
    models/
    └─face-emotion/
      └─config.pbtxt
      └─1/
        └─model.savedmodel/
          └-keras_metadata.pb
          └-saved_model.pb
          └─assets/
          └─variables/
            └─variables.data-00000-of-00001
            └─variables.index
```

# Deploy

## Clone the repo

- Clone the repo (`git clone ...`)
- If there's permission issues with gitlab, generate ssh keys (`ssh-keygen`) and add them to github account
- CD into the folder (`cd cloned-repo`)
- Create the `.aws.env` file in the root of the repo with the following:

```
AWS_ACCESS_KEY_ID=SOME_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=SOME_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION=us-east-1
```

# Triton server

- Running the triton server alone

```bash
docker run --env-file .envs3 -p8000:8000 -p8001:8001 -p8002:8002 --rm --net=host nvcr.io/nvidia/tritonserver:22.06-py3 tritonserver --model-repository=s3://triton-repository/models/
```

# Docker Compose

- Add triton to the `docker-compose.yaml` with image, env file, ports and command.
- Run all the endpoints and triton server (`docker-compose -f docker-compose.yaml up --build`)
- Create a request with docs (<http://ec2.ip.address:8000/docs>)
