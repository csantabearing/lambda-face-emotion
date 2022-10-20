# Deployment on EC2

## Create EC2 Instance

- Go to EC2 console: <https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1>
- Create EC2 instance
- Pick deep learning ami
- Pick instance type: At least p3.2xlarge
- Create key-pair
- Download key
- Edit network
- Enable IPV4 address
- Open ports 8000-8004 from anywhere
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

- Install the requirements (`pip install -r requirements.txt`) the pip and python version might be different
- Create data directory (`mkdir data`)
- Download and uncompress the training data in the data folder

```
wget https://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz
wget https://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz
tar -xzf images.tar.gz
tar -xzf annotations.tar.gz
```

- Train the model (`python train.py`)
- Run ml-flow ui (`mlflow ui --port 8004 --host 0.0.0.0`)
- Configure awscli (`aws configure`)
- Upload the model to the s3 model repository

```
aws s3 cp --recursive segmentation s3://triton-repository/models/pet-bokeh/1/model.savedmodel/
```

- Upload the config

```
aws s3 cp pet-bokeh/config.pbtxt s3://triton-repository/models/pet-bokeh/config.pbtxt
```

# Docker Compose

- Add triton to the `docker-compose.yaml` with image, env file, ports and command.
- Run all the endpoints and triton server (`docker-compose -f docker-compose.yaml up --build`)
- Create a request with docs (<http://ec2.ip.address:8000/docs>)
