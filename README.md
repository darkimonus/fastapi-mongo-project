## About
This is a FastAPI application that provides an API for restaurants, enabling frontend applications (websites or mobile apps) to offer customers a convenient service with the following features:

- Menu browsing  
- Order payment  
- Viewing order history (including the price and nutritional value of each item)
- Table reservations  
- Additional features are likely to be added in the future  

The API also provides administrative endpoints, allowing users to generate and view statistics, add dishes, tables and restaurants. The API is designed to support a seamless service for an entire restaurant chain.

## Technologies

- MongoDB is used for data storage in combination with Motor.  
- Docker and Makefile are used for development and deployment.  
- Poetry is used for dependency management.  
- Redis is used as a message broker and caching tool.  
- Celery is used for interacting with services that provide SMS messaging and task scheduling.  
- Security is ensured using CORS and JWT tokens.  


## Setting up

Firstly you need to configure .env file in source directory. You can see example in .env-sample.  
To run the app use make commands below:  
- build-app : builds docker images and starts containers.  
- up : starts containers.    
- stop : stops containers.    
- restart : restarts containers.    
- poetry: does all poetry commands without needing to go to source dir
