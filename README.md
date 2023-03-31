# Flask web server and telegram bot
### Registration users from bot
Link - [test-app-flask2023.herokuapp.com/](https://test-app-flask2023.herokuapp.com/)
Bot link - [_BOT_](https://telegram.me/fgjghjkhgkhgkhjkjhk_BOT)
___
## Content
 - [Technologies](#what-we-used)
 - [Desription](#what-we-do)
 - [Star Project](#how-to-start-project)

___
## What we used?
_Technologies used_: Flask, Aiogram, Flask_login, SQLAlchemy, multiprocessing, 
Flask_wtf, PostgresQL, Heroku Deploy, Render Deploy


## What we do?
Made a web application. User registration is carried out through the telegram bot. 
The bot, having received data from you, creates a user for the web application in the database. 
These data are used to enter the site.


## How to start project?
1. Run `git clone {SSH-link from GitHub}` on your PC;
2. Run `pip install -r requirements.txt`;
3. Create '.env' file and write to it the enviroment variables:
	- SECRET_KEY (Fot example: '*jfjn&nf8jfghg=fgkhd6k56566')
	- FLASK_DEBUG (when deployed to the server, set the value to 0)
	- DB_CONNECT 
	- BOT_TOKEN 
	- BOT_ID 
4. Run `alembic upgrade head`;
5. To start the service locally, use the command `python3 run.py`;