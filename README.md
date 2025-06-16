Flask To-Do App (Dockerized & Deployed on AWS EC2)

This project is a simple Flask-based To-Do list application, containerized using Docker and deployed on an AWS EC2 instance running Amazon Linux 2.
Features

        •	Add tasks to a list
        •	View and manage tasks
        •	Fully dockerized
        •	Hosted on an EC2 instance
Live Demo

    http://13.203.67.226
    
Tech Stack

        •	Python with Flask
        •	HTML/CSS (Bootstrap)
        •	Docker
        •	AWS EC2 (Amazon Linux 2)
 Project Structure
 
	flask_todoapp/
	├── app.py
	├── requirements.txt
	└── Dockerfile

 Deployment Steps
•	Clone the project:

    git clone https://github.com/RishitSharma88/flask_todoapp
    cd flask_todoapp

•	Create requirements.txt:

    Flask==2.3.3
    Werkzeug==2.3.7

•	Create Dockerfile:

    FROM python:3.9-slim
    WORKDIR /app
    COPY . .
    RUN pip install -r requirements.txt
    EXPOSE 5000
    CMD ["python", "app.py"]

•	Build Docker Image:

    docker build -t flask-todo-app .

•	Run Docker Container Locally:

    docker run -d -p 5000:5000 flask-todo-app
  <img width="452" alt="image" src="https://github.com/user-attachments/assets/f40f6fad-2a24-4d51-9e7d-2f3e294b43f6" />


 

•	Upload App to EC2:

    scp -i todoapp.pem flask_todoapp.zip ec2-user13.203.67.226:~/

•	Connect to EC2:

    ssh -i todoapp.pem ec2-user@13.203.67.226

•	Install Docker on EC2 :

    sudo yum update -y
    sudo yum install docker -y
    sudo service docker start
    sudo usermod -a -G docker ec2-user

•	Unzip and Build on EC2:

    unzip flask_todoapp.zip
    cd flask_todoapp
    docker build -t flask-todo-app .

•	Run Container on EC2:

    docker run -d -p 80:5000 --name todo-container flask-todo-app


Access the App
  Open a browser and go to:
  http://<your-ec2-public-ip>
  Example: http://13.203.67.226
   
<img width="452" alt="image" src="https://github.com/user-attachments/assets/965f8255-57e3-4fcb-bf26-06c878f6bf1c" />
<img width="452" alt="image" src="https://github.com/user-attachments/assets/808040f5-a5a4-48a9-b124-a1aeaa44aa35" />
<img width="452" alt="image" src="https://github.com/user-attachments/assets/8e0c4b01-8620-444c-bbcd-8caa09d4162c" />


deploy.sh – Shell Script for App Setup

	Created a deploy.sh script to:
		•	Pull the Docker image
		•	Stop and remove any existing container
		•	Run the container with the appropriate ports
		•	The script automates the deployment process in a single command.
  deploy.sh:

	#!/bin/bash
	echo "Ri****(password)" | sudo docker login -u rishit***(username) --password-stdin
	
	sudo docker pull rishit****(username)/flask-todo-app:latest
	sudo docker stop todo-container || true
	sudo docker rm todo-container || true
	
	sudo docker run -d -p 5000:5000 --name todo-container rishit****(username)/flask-todo-app:latest
	
	echo "App deployed and running on port 5000"

 Give permissions to execute file:

	 chmod +x deploy.sh

 Run deploy.sh using:

	 ./deploy.sh

  Amazon S3 Access via EC2 (IAM Role)

  	•	Created an S3 bucket named <todolistapp123.
	•	Uploaded an object flask_todoapp.zip to the S3 bucket.
	•	Attached an IAM role to the EC2 instance with the necessary S3 read permissions (e.g., AmazonS3ReadOnlyAccess).
 Verified S3 access from within EC2 using:

	 ssh -i todoapp.pem ec2-user@<PUBLIC-IP>
	 aws s3 cp s3://todolistapp123/flask_todoapp.zip .
	 docker build -t flask-todo-app .
	 docker run -d -p 80:5000 flask-todo-app
  <img width="1470" alt="Screenshot 2025-06-16 at 09 24 21" src="https://github.com/user-attachments/assets/00987e82-85f0-42c0-ad10-789dfd603b1a" />
  <img width="1470" alt="Screenshot 2025-06-15 at 13 38 53" src="https://github.com/user-attachments/assets/5dc631b5-5b3a-402d-888e-d239bfafba5d" />
  



 




