# q-yaar
Get out to play.

## ***Project Specs***
* Ubuntu 22.04 (Preferred)
* Python - 3.11.9
* Django - 5.0.7
* Postgres - 16.3
* Docker - Follow the [link](https://docs.docker.com/get-docker/)
* Docker Compose - Follow the [link](https://docs.docker.com/compose/install/)
* Redis

## ***Setup on Windows (Using WSL)***
*WSL allows you to run a Linux environment on Windows. This is the preferred way to run the project on Windows.*

#### 1. WSL Installation

Open PowerShell/Terminal as an administrator and run the following command:

```bash
wsl --install
```

This will install WSL2 and Ubuntu 22.04 on your system by default.
Incase you face any issues refer to this [link](https://docs.microsoft.com/en-us/windows/wsl/install).

#### 2. Ubuntu Setup

1. Open Ubuntu 22.04 from the start menu or just run the following command in PowerShell/Terminal:
    ```bash
    wsl
    ```
2. Set up a username and password.
3. Update and upgrade the packages by 

    ```bash
    $ sudo apt update
    $ sudo apt upgrade
    ```
4. Install python3.11 and set it to default by running the following commands:

    ```bash
    $ sudo apt install software-properties-common
    $ sudo add-apt-repository ppa:deadsnakes/ppa
    $ sudo apt install python3.11
    $ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
    $ sudo update-alternatives --config python3
    ```
5. Setup Postgres:

    *Follow the steps in section - Setup Postgres in the Local Setup section below. Just make sure you're in the Ubuntu terminal.*

#### 3. Setup Docker 
Install docker desktop for windows from [here](https://docs.docker.com/get-docker/). In the settings make sure you have WSL2 as the default engine.

#### 4. Setup VSCode WSL Remote Connecction
1. Install the Remote - WSL extension in VSCode. This will allow to run VSCode in the WSL environment.
2. Pull your repository in the WSL environment and open it in VSCode.
3. Everything will now run in linux environment but you can enjoy the GUI of VSCode in windows.

Windows setup is done, for running the project follow the steps in the Local Setup section below.




## ***Setup on Local***

### Setup Postgres
```bash
$ sudo su - postgres 
$ psql -p 5434 # (Or whichever port runs your postgres 16.3) This will open psql shell, follow these commands

CREATE DATABASE q_yaar_db;
CREATE USER q_yaar_user WITH PASSWORD 'q_yaar_password';
ALTER ROLE q_yaar_user SET client_encoding TO 'utf8';
ALTER ROLE q_yaar_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE q_yaar_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE q_yaar_db TO q_yaar_user;
ALTER ROLE q_yaar_user SUPERUSER;
ALTER ROLE q_yaar_user CREATEDB;
```
Connect to DB from command line using psql
```bash
psql -d postgres://q_yaar_user:q_yaar_password@localhost:5434/q_yaar_db # Use the applicable port number
```

### Create a Virtual Environment
Make sure you're in the directory - q-yaar
```bash
$ python3 -m venv .venv  # This will create a virtual environment
$ source .venv/bin/activate  # You can see the virtual environment is active
$ cd q_yaar_platform
$ pip install -r requirements-dev.txt # This will install all the requirements
```

### Setup .env File
Make sure you're in the directory - q_yaar_platform
```bash
$ touch .env
```
Now copy and paste the contents available in the file - env_example <br />
Ask someone for the actual env values

### Setup Docker and Start Redis Server
Make sure you're in the directory - docker
```bash
$ sudo docker-compose -f docker-compose-dev.yml up -d q_yaar_redisearch
```

If you want to stop the Redis server
```bash
$ sudo docker-compose -f docker-compose-dev.yml down
```

### Run the Django Server
Make sure you're in the directory - q_yaar_platform

```bash
$ python manage.py migrate
$ python manage.py runserver
```
You should see your server running on __127.0.0.1:8000__ 

### Create a Superuser to get Admin Access
Make sure you're in the directory - q_yaar_platform
```bash
$ python manage.py createsuperuser
```
Follow the instructions on the screen to create a superuser <br />
Ensure that you enter a valid uuid during superuser creation

### Try logging into admin
Open the following url in your browser - __127.0.0.1:8000/admin/__ <br />
Login using the username and password entered during superuser creation <br />
You can now access all the models through django admin

## ***Formatting***
Use black (already mentioned in requirements.txt) <br />
Make sure the line length arg is set to 119 (it defaults to 80 if nothing is set)

* For VScode, add the below configs to your settings.json file

```
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": false,
    "python.languageServer": "Pylance",
    "python.formatting.provider": "black",
    "python.linting.flake8Args": [
        "--max-line-length=119"
    ],
    "python.formatting.blackArgs": [
        "--line-length=119"
    ],
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter"
    },
    "black-formatter.args": [
        "--line-length",
        "119"
    ],
    "python.autoComplete.extraPaths": [],
    "python.analysis.extraPaths": [
        "q_yaar_platform"
    ]
}
```

### Running dev server with Docker
From the project root run the follwing command
```bash
$ sudo docker-compose -f docker/docker-compose-dev.yml up -d
```
To crate superuser inside the docker container
```bash
$ docker exec -it docker-q_yaar_core-1 /bin/bash
```
Now create a super user
```bash
$ python manage.py createsuperuser
```

