URL Shortener
==========

##Using Flask and Redis

The libraries needed in order to run this program is listed in the 
'requirements.txt'. You should install them in a virtualenv. The major ones are Redis, Flask and Requests.

After you installed the libraries, run your Redis server by using the command `redis-server -port 8888`. You can change the port number in the config.py file by changing the `DB_PORT` variable. Right now, it is set to 8888.

After starting the Redis server, run `python run.py` and it should launch my app in localhost:5000.



