<h3 align="center">Projects Reminder Api</h3> </p>
Table of contents

1 About the Project<br> 2 General Preview<br> 3 Technical<br> 4 To Do List<br> 5 Contributing<br> 6 License<br> 7 Versions<br> 8 Contact Information<br>

👇 👇 👇 👇 👇

Prequisite

<p>

Before running the project please ensure you have uvicorn installed and started the server in your system . That is in your terminal type $ uvicorn app.main:projectsapi --reload

</p>
About the App

<p> An python api application made using  [FastaPi] (https://fastapi.tiangolo.com/) framework. The api enables a user to document projects which he/she has already done or which he/she is planning to do in the future.<br>The api's architecture is isnpired by the mvvm pattern thus addressing the seperation concerns.<br> </p> share ... 😉
Technical

How to use

The app is divided into 6 parts: The api, The core,crud, schemas, models & database

<b> The Schemas </b>

These are basically python objects  used to hold data which is presented to the user in form of responses. The schemas play two roles: They are used by pydantic library to convert the python objects into Body responses, which are then conveyed to the frontend that is the user. Their second role is to convey the data given by the user to the sqlalchemy orms . 

<b> The Models </b>

The models are sqlaclhemy orms which represent tables stored in the database. The models are the ones which interact with the database directly. They essentially, turn the data held by the schemas into sqlalchemy understable data types. Then they are stored into the database.

<b> The Db </b>
This folder contains files which are used to initialize the database. Essentially, the base class is inherited by the sqlalchemy orms and the session object is then used to create a connection with the db for a single request. A request in this case refers to the process of querying the database.  

<b> The crud </b>

This folder contains files which in turn contains the query commands used by the api end points. Both, the crud_user and crud_project inherit from the crud_base class. The crud base class defines the standard crud operation methods which are going to be used by both classes to access and modify the data. The reason for seperating the two classes is to make debbugging and testing easier and to reduce repetition.

<b> The core </b>

This contains files which serve as configuration/ settings for our api application. The Settings class contains the constants used through out the application like the sqlalchemy-database-uri etc. The security file on the hand is responsible for generating the jwt tokens needed when a person is logging in. 

<b> The api </b>

This is the backbone of the application. It is where the api endpoints live :-). The dependency file provides all the needed dependencies to the api components thus it carries out the role of DI. The api file's work is to route the paths and create tags for them. The routing in this case is similar to Flask's Blueprint library. The end points folder contains three files: The login, the projects and user files. The login file contains the end point needed to access the token. The token (jwt token) is needed in order to activate a user. When a user registers, his account is inactive at the start, after logging in and acquiring a token, the user becomes active. Note:The token serves as a security measure to prevent unauthorized actions .That is since  it's signed when the api receives a token that it emitted, it then verifies that it actually emitted it  before allowing the user to carry out an operation eg see all users. The project file on the other hand exposes the end points needed to create,delete, update and read projects for a specific owner. Likewise, the user file.

You can:

a. Clone the project and run it yourself in Pycharm(Most up to date)

### Running the project 1. Required to run project:

    Use Pycharm ide/ Vs Code Editor (whichever python ide anyway :-) ).

2. Clone this repository:

`git clone https://Gibson_Ruitiari@bitbucket.org/Rui123G/projects-reminder-api.git`

3. open Project in Pycharm/ Vs Code

4. Start the uvicorn server then head over to your browser and insert the following link (http://127.0.0.1:8000/docs) to access the interactive api documentation. This enables you to view and and test the end points. You can also use Post man to test the end point. If using terminal you can also use curl 

5. Incase of an eror when building project, install the necessary dependencies
Libraries/ Frameworks used


    Fast Api framework- FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. (https://fastapi.tiangolo.com/)
    
    click - a python framework used for creating beautiful command line interfaces (https://click.palletsprojects.com/en/7.x/)
    
    Uvicorn- a lighting fast asgi server built on top of uvloop
    
    PJwt - jwt python version, used to generate jwt tokens and verify the tokens.
    
    Passlib- a library used for hashing and verifying the passwords 
    
    SqlAlchemy -SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL (https://www.sqlalchemy.org/)

To Do List

🚧 🚧 Use postgress instead of sqlite, add a project timeline feature  & upload the api to heroku/aws
Contributing

I would love to have your help in making this api better. The project is still very incomplete, but if there's an issue you'd like to see addressed sooner rather than later, let me know.

Before you contribute though read the contributing guide here: CONTRIBUTING GUIDE

For any concerns, please open an [issue] or JUST, fork the project and send a pull request.
License
Assets

Credits: - Logo is used from FreePik

Open Source Love
Created by a geek for geeks :-)
Versions

Version 1.0 DATE 28/05/2020
Contact Information

    Gmail : [gibsonruitiari@gmail.com]

<hr>

:bowtie: ✌ 