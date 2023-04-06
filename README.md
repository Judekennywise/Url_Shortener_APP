# Url_Shortener_APP

This is a ulr shortener app built with FASTAPI

Here’s a summary of the URL shortener’s API endpoints:
| Endpoints | Http verb | Request body | Action
| --- | --- | --- | ---|
| / | GET | | Returns a Welcome message string
| /url | PoST | Your target url | Returns the shortened Url in the following string format {"target_url": string, "is_active": bool, "clicks": int, "url": string, "admin_url":string}
| /admin/{secret_key} | GET | | Returns Admin info in the followin format {"target_url": string, "is_active": bool, "clicks": int, "url": string, "admin_url":string}
| /admin/{secret_key}	| DELETE | | Deletes the shortened url ny setting "is_active" to false

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
