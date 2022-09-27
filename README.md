# Deployment on EC2

Go to EC2 console: https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#
Create EC2 instance
Pick amazon linux
Pick instance type: At least t3.medium
Create key-pair
Download key
Edit network
Enable IPV4 address
Open port 5000 from anywhere
Launch Instance
Get the ip address of the instance
Change key permissions to 400
SSH into the machine (ssh -i key.pem ec2-user@ec2.ip.address
Install git if needed (sudo apt install git for ubuntu based distros, sudo yum install git for amazon linux)
Install pip if needed
Clone the repo (git clone ...)
If there's permission issues with gitlab, generate ssh keys (ssh-keygen) and add them to github account
CD into the folder
Install the requirements (pip install -r requirements.txt)
Run the api (uvicorn app:app --host 0.0.0.0)
Run with docs (ec2.ip.address:5000/docs)
Run with postman