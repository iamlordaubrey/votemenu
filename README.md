# Menu Vote

Description: An API to vote on restaurant menus

### Limitations
The v2 endpoint doesn't calculate the vote result; it currently uses v1's logic.
v2 needs to use a weighted average of the columns in determining the result.

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
/vote           : Vote (and result) endpoint

/docs           : Documentation
/redoc          : Documentation
```
