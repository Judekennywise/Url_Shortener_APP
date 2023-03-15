# Url_Shortener_APP

This is a ulr shortener app built with FASTAPI

Follow these commands to run the project on your local machine :

Open your terminal

Clone the project 
```
https://github.com/Judekennywise/Url_Shortener_APP.git
```

Enter the project directory 

```
cd Url_Shortener_APP
```

Create a virtual env

```
python -m venv env 
```

Activate your env(for windows)

```
env\Scripts\activate 
```
(for linux or mac)

```
source env/bin/activate 
``` 

Install Project Dependencies

```
pip install -r requirements.txt
```

Note that this project uses environmental variables, to setup environmental variables
Create a .env file inyour root directory and add the following variable formats:
ENV_NAME="Your environment name"
BASE_URL="The project URL" :If you're running the project on your local computer the url should be "http://127.0.0.1:8000"
DB_URL="sqlite:///./shortener.db" you can maintain this database url or change the name from "shortener.db" to any of your choice.

Run the project

```
uvicorn shortener_app.main:app --reload
```
