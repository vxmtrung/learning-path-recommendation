# PERSONALIZED LEARNING PATH RECOMMENDATION - BACKEND DEVELOPMENT
- This is backend development part for **Personalized Learning Path Recommendation**

# How to run?

## Prepare environment
- **Python Version:** 3.12

- **Framework:** Django RestFramework *(This framework will be installed through installing packages)*

- **Pre install Python Library:**
    - pip 
        - *This library allows us to install another packages/libraries in Python*
    - pipenv 
        - *This library allows us to create a virtual development environment for Python, which means all packages/libraries installed won't effect to global pip/python*

- **Package Manager:**
    - We will manage packages/library by using ***Pipfile*** and ***Pipfile.lock***

- **Others:**
    - Docker and Docker Compose
    - If you're using Linux-based OS, please install ***libpq-dev*** *(for Debian/Ubuntu)* or ***libpq-devel*** *(for Centos/Fedora/Cygwin/Babun)* package on your OS.

## Create development environment
- **All steps below is run at root directory of this repo.**

- **Copy environment file**
    - Running this command line to create a **.env** file *(then modify it if you like)*
    ```
    cp .env.example .env
    ```

- **Setup database and tools with Docker**
    - Use this command line to pull image and run database with tool instances.
    ```
    docker compose up
    ```
    or 
    ```
    docker-compose up
    ```
    depends on your Docker Compose version.

- **Database tools Login information**
    - ***Adminer:*** Open http://localhost:8080
    > System: PostgreSQL

    > Server: postgres

    > Username: admin

    > Password: 123456
    - ***PgAdmin4:*** Open http://localhost:8888
    > Email Address: admin@email.com

    > Password: 123456

        - Choose **Add New Server**

            - Tab General:
    
    > Name: localhost

            - Tab Connection:
    > Hostname/Address: postgres

    > Port: 5432

    > Username: admin

    > Password: 123456

        - Click Save

    - Remember that if you modify **.env** before running **Docker Compose**, you have to change login information appropriately.

- **Install Packages/Libraries**
    - First, go to the **backend** folder on Terminal
    ```
    cd backend
    ```

    - Install Packages/Library:
    ```
    pipenv sync
    ```

    - Then, move to ***pipenv*** environment for development on Terminal:
    ```
    pipenv shell
    ```

    - Check if all dependencies have been installed to your virtual environment? *(Remember to run **pipenv shell** before)*
    ```
    pip list
    ```

## Run Migration
- **First, make sure you're in *backend* folder, not root directory of repo and your database is running in Docker**
- **Then, run this command line to generate migration:**
```
python manage.py makemigrations
```
- **Finally, run this command line to migrate to your database**
```
python manage.py migrate
```

## Run Project
- **First, make sure you're in *backend* folder, not root directory of repo, database is running in Docker and migrations have been applied.**
- **Then, run this command line to run project:**
```
python manage.py runserver
```
- **The project will run at: http://localhost:8000**

## Install new Packages/Libraries
- **First, make sure you're in *backend* folder**
- **Then, run this command line:**
```
pipenv install <package-name>
```