# Deployment on EC2

## Create EC2 Instance

- Go to EC2 console: https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#
- Create EC2 instance
- Pick amazon linux
- Pick instance type: At least t3.medium
- Create key-pair
- Download key
- Edit network
- Enable IPV4 address
- Open port 8000 from anywhere
- Launch Instance

## Install dependencies
- Get the ip address of the instance
- Change key permissions to 400
- SSH into the machine `ssh -i key.pem ec2-user@ec2.ip.address`
- Install git if needed (`sudo apt install git` for ubuntu based distros, `sudo yum install git` for amazon linux)
- Install pip if needed (`sudo apt install python3-pip` for ubuntu based distros, `sudo yum install python3-pip` for amazon linux)
- Clone the repo (`git clone ...`)
- If there's permission issues with gitlab, generate ssh keys (`ssh-keygen`) and add them to github account
- CD into the folder (`cd cloned-repo`)
- Install the requirements (`pip3 install -r requirements.txt`)

## Run API
- Run the api (`uvicorn app:app --host 0.0.0.0`)
- Create a request with docs (http://ec2.ip.address:8000/docs)
