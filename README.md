# simple-Python-CRUD-TDD

## Simple CRUD in Python with TDD focus
### Notes
1) implementation has been done with Python3, Flask, SqlAlchemy, Postgres and PyTest
2) mypy is used for linting on the spot
3) DB management is intrinsic and doesn't require attention
4) as requested, all software is made in containers with docker/docker-compose

### Installation
    git clone https://github.com/silpol/simple-Python-CRUD-TDD
* command above will clone code into target directory from GitHub


    cd simple-Python-CRUD-TDD
* change to current directory


    docker compose up -d db
    docker ps
* launch DB container as detached and check it runs, it should look like


    CONTAINER ID   IMAGE         COMMAND                  CREATED       STATUS       PORTS                                       NAMES
    
    d3e53409e4fb   postgres:12   "docker-entrypoint.s…"   9 hours ago   Up 9 hours   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   db
---
    docker compose up --build pythonapp
* launch application build and run it. Option --build is not critical for first run, but gets useful once you start and stop it, e.g. for debugging.
* you can check in another terminal how both containers run with **docker ps -a** 
* it will look like this:



    CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS         PORTS                                       NAMES
    
    a62b7bea453b   pythonapp     "flask run --host=0.…"   5 seconds ago   Up 5 seconds   0.0.0.0:80->80/tcp, :::80->80/tcp           pythonapp
    
    d3e53409e4fb   postgres:12   "docker-entrypoint.s…"   9 hours ago     Up 9 hours     0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   db 

---
* repetitive run produces a lot of dangling images. Clean up is, type 


    docker image prune
and then **y** to confirm.

* when you stop application with Ctrl+C keys, it leaves DB container running with persistent database stored in Postgres.
* You can check it with command PSQL (you will be in context of it)

 
    docker exec -it db psql -U postgres

and then check list of tables with PSQL command \dt
also you can check separate tables with commands:

    select * from continents;
    select * from countries;
    select * from cities;

exit is with command **exit** or **\q** or pressing Ctrl+D

## Running testbed
* testing is done with **Pytest** with [pytest-docker-compose](https://github.com/pytest-docker-compose/pytest-docker-compose/blob/develop/README.rst) plugin
* to make containers persist beyond a single test is to supply the --use-running-containers flag to pytest like so:


    pytest --use-running-containers
## To Finish (aka tech debt)
* finalize cascade deletion - [issue](https://github.com/silpol/simple-Python-CRUD-TDD/issues/1) #1
* write rest of automated tests - [issue](https://github.com/silpol/simple-Python-CRUD-TDD/issues/2) #2

## Future options
* separate views and models into separate modules
* add cleanup routine to docker-compose

# CLEAN UP afterwards, there is no **clean** routine yet
