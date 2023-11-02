## Docker

Docker is a software platform that allows you to build, test, and deploy applications quickly. Docker packages software into standardized units called containers that have everything the software needs to run, including libraries, system tools, code, and runtime.

## Why Use Containers for Machine Learning?

Running an ML model on the computer is an easy task. But when we want to use that model at the production stage in other systems, it’s a complex task. Docker makes this task easier, faster, and more reliable.

## How to Deploy the ML Model Inside a Docker Container?

To understand how to deploy our Machine Learning model inside a Docker container, we will take a simple Titanic dataset Machine Learning model to illustrate the workflow.

1. Create a separate directory for this task and copy your Machine learning code to that directory.

2. Create a Dockerfile.

### What’s a Dockerfile?

It’s just a way to create your own customized Docker image. This file contains step-by-step requirements as per our use case. Simply Dockerfile is a script on a recipe for creating a Docker image. It contains some special keywords such as `FROM`, `RUN`, `CMD`, etc.

Now let us understand the code inside Dockerfile.

- `FROM`: This is used for providing the name of the base image on which we’ll be adding our requirements. Here, I have used Python as a base image for the container.
- `COPY` command will copy the specified files from the local machine to the container that will be launched using this image.
- `RUN` it’s a build time keyword, and any program that goes with it will be executed during the building of the image.
- `CMD`: It’s a runtime keyword. Any program one command goes with it will be executed when the container is launched.

3. Python Code

This python code will be run as soon as our container starts. Here we have used the joblib module in python through which we can save and load our trained models.

```python
import joblib

classifier = joblib.load('survive_prediction.pkl')
print("Enter the following details to make the predictions:- ")

pclass = int(input("Enter The Pclass:- "))
Age = int(input("Enter The Age:- "))
SibSP = int(input("Enter The SibSp:- "))
Parch = int(input("Enter The Parch:- "))
Sex = int(input("Enter The Sex:- "))

passenger_prediction = classifier.predict([[pclass, Age, SibSP, Parch, Sex]])

if passenger_prediction == 0:
    print("Not Survived.")
else:
    print("Survived")
```

4. Now, we will be going to build the image from the Dockerfile that we have created just above. To build the image we use the following command:
```docker build -t image_name:version```

5. Now Finally, we are ready to launch our container and run our machine learning model:
```docker run -it --name titanic_survivors titanic_model:v1```

-> When we run this command, a new environment is launched; a new OS entirely. So behind the scene, docker-engine does a lot of tasks such as providing a network card, storage, a complete new file system, RAM/CPU, etc. These are with respect to an OS.

-> So if you want to see the entire details of the container, you can use:
```docker info container_name```

-> With this command, you can see the entire details of the container like, how much storage it is using, what’s the network card and many more.

6. Using CLI (Command Line Input) we can give input to our python code. By command-line input means through the keyboard we can pass input to the container.