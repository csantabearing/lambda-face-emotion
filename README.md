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
- Launch Instance
- SSH in the instance

## DVC

- Install pip (`yum install pip`)

- Install DVC with (`pip3 install dvc`)

- Initialize DVC (`dvc init`) in your repo

- Add files to git (`git add .dvc`)

- Add files to git (`git add .dvcignore`)

- Commit changes to git (`git commit -m "dvc init"`)

- Create a data folder (`mkdir data`)

- Enter the data folder (`cd data`)

- Download the pets dataset:

```
wget https://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz
wget https://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz
```

- Add the raw image data to dvc (`dvc add data/images.tar.gz`)

- Add files to git (`git add data/images.tar.gz.dvc data/.gitignore`)

- Add the raw annotation data to dvc (`dvc add data/annotations.tar.gz`)

- Add files to git (`git add data/annotations.tar.gz.dvc data/.gitignore`)

- Commit changes to git (`git commit -am "Raw data"`)

- Add s3 remote (`dvc remote add -d storage s3://triton-repository/data/`)

- Add config to git (`git add .dvc/config`)

- Commit changes in git (`git commit -am "DVC Storage"`)

- Push data with dvc (`dvc push`)

- Uncompress the dataset

```
tar -xzf images.tar.gz
tar -xzf annotations.tar.gz
```

- Add files (`dvc add data/images`)

- Add to git (`git add data/.gitignore data/images.dvc`)

- Add files (`dvc add data/annotations`)

- Add to git (`git add data/.gitignore data/annotations.dvc`)

- Commit changes to git (`git commit -am "Uncompressed data"`)

- Push data with dvc (`dvc push`)
