To run this program you need Xampp or equivalent way to host MySQL database

Software is build with FastAPI framework and uses sqlalchemy to connect to database.
That way you only need to setup a fresh db and then sqlalchemy will set up the db at first usage.

To run this program take these steps:

Use Xampp or equivalent to create your base db and name it i.e. sixsaudit (needs to be an MySQL db)

1. Open folder in the editor of your choice
2. Create.env
    create a new file to the project root and name it .env
    copy lines from .envexample and paste to .env 
    Give random string to JWT_SECRET at .env
    add direct path to your fresh db to CONNECTION_STRING at .env after mysql+mysqlconnector:// text
2. Install packages
    Make sure you are in virtual environment
    Open command prompt and navigate to the root of this project
    Run command pip install -r requirements.txt
    This will install required packages from requirements.txt
    This way you are sure that you have all required packages
3. Create static folder
    Create new folder to the root of the project and name it static
    In this folder API stores all static files that are uploaded to server
4. Create SSL HTTPS for Localhost
    Follow this tutorial, create the mentioned cert -folder to the project root and continue there with the tutorial.
5. Run program
    Make sure you are at the project root and run command python main.py
    Open the app from the link shown at terminal
    Navigate to /docs page (i.e. localhost:8002/docs)
    You should see an API documentation now
