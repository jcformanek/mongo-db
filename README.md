# Mongo DB Assignment
University of Cape Town CS Honours Assignment


## Quick start

### Run a Mongo DB instance in a docker container
If you have never used docker before, just go install it here:
https://docs.docker.com/docker-for-windows/install/

Once docker is installed, run the following comands in your shell to get a container with Mongo DB up and running:

$ docker pull mongo

$ docker run -d -p 27017:27017/tcp --name my-mongo mongo:latest

## Run the python script to import the data into the db
You will need to install the pymongo package

$ pip install pymongo

The python script creates a new database and loads the books data into it.

## Use the Mongo Comanad Line Interface (CLI) to explore the DB
To use the Mongo CLI simply run the following comand to get a bash shell inside the running container.

$ docker exec -it my-mongo bash

Then run the following comand to start the mongo CLI

$ mongo

## Use the tutorial on vula 
The tutorial on vula shows you all the mongo comands.

## Exit the CLI
simply type:

$ exit

$ exit

# Using the telegram bot
Create a file called token.txt and include the telegram token on the first line of the file. 

$ pip install python-telegram-bot --upgrade

# Sources
The Books Dataset was obtained here: https://github.com/ozlerhakan/mongodb-json-files

Information on the mongo docker image can be found here: https://hub.docker.com/_/mongo

Use the W3 Schools tutorial to extened the python script: https://www.w3schools.com/python/python_mongodb_getstarted.asp
