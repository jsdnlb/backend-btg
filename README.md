# Backend BTG Pactual

This project was developed in order to provide a solution to the technical test that consists of developing both the backend with FASTApi and Dynamo DB and the frontend with React

## How to start?🚀

_These instructions will allow you to get a copy of the project up and running on your local machine for development and testing purposes._

### Installation 🔧

First we must clone the repository, access the folder and then create a virtual environment to install all the necessary libraries.

```
git clone https://github.com/jsdnlb/backend-btg.git
cd backend-btg
python3 -m venv venv # Create virtual environment
source venv/bin/activate # Activate environment, may vary in other os
```

Once the environment is active we can install requirements

```
pip install -r requirements.txt
```

Create the .env file to the root of the project

With this we would have everything necessary to run the project and see the magic.

```
uvicorn main:app --reload --env-file=".env"
```

## Running endpoints 🔐

Just enter the documentation [Swagger](http://localhost:8000/docs#/) to start using it.

Here you will find some endpoints to create clients and obtain them, the same for funds and for transactions, in addition you will find two endpoints to subscribe or cancel a fund.

![image](https://github.com/jsdnlb/backend-btg/assets/17171887/91542a48-5654-4dd6-94d6-0ee6605388c6)

## Deployment in production 🚀

To deploy the server you only have to re-generate the image with Docker locally and update it in the management that containers, you can find more information in the file guidence.sh since there is a stack in CloudFormation you will not have to do anything additional, however in the file fastapi-backend-btg.yaml you can see how it was deployed, you would simply have to change the account_id


## Built with 🛠️

_This project was built with the following tools_

* [Python](https://www.python.org/) - Programming language
* [FastAPI](https://fastapi.tiangolo.com/) - Framework
* [DynamoDB](https://aws.amazon.com/es/dynamodb/) - DynamoDBServerless, NoSQL, fully managed database
* [Docker](https://www.docker.com/) - Accelerated Container Application Development
* [AWS CloudFormation](https://aws.amazon.com/cloudformation/) - Infrastructure as code
* [Unittest](https://docs.python.org/3/library/unittest.html) - Unit testing framework

## Wiki 📖

Once you have the project running you can run it in a simple way here: [Swagger](http://localhost:8000/docs#/) and find the documentation in a more visual way here [OpenAPI](http://localhost:8000/redoc) , although in theory both have the same information.

## Things to improve 🌟

* Add SonarQube
* Add more and improve test cases
* Add Makefile

## Developer by ✒️

* **Daniel Buitrago** - Documentation and programming - [jsdnlb](https://github.com/jsdnlb)

---
