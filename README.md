# Menu Vote

Description: An API to vote on restaurant menus

### Assumptions

### Tech Stack
Built using the FastAPI framework. Libraries are kept as minimal as possible. 

Runtime: Python 3.10.0 (can be found in `.python-version` file)


## Install #
Creates a fresh virtual environment (called .venv) and installs requirements
```commandline
make setup
```

## Run #
Run a single instance of the uvicorn server for local development

Install pip requirements
```commandline
make pip_sync
```

Run server
```commandline
make runserver
```

Run tests
```commandline
make runtest
```

# Docker #
To run the application using docker
```commandline
docker-compose up
```

To rebuild the image, then run the application
```commandline
docker-compose up --build
```


# Available Endpoints #
```json lines
/               : Main application endpoint
/status         : Healthcheck status endpoint
/status/version : Application version

/restaurant     : Restaurant endpoint
/employee       : Employee endpoint
/menu           : Menu endpoint

/docs           : Documentation
/redoc          : Documentation
```
