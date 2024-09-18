### Prerequisites

1. Docker ( https://docs.docker.com/engine/install/ )
2. Docker compose ( https://docs.docker.com/compose/ )
3. Make ( https://www.geeksforgeeks.org/how-to-install-make-on-ubuntu/ )

### Commands

- `make build` : build docker image
- `make up` : start docker containers
- `make down` : down docker containers
- `make test` : launch tests with `pytest`
- `make shell` : shell into docker container
- `make logs` : attach container logs to your terminal
- `make re` : down and reup containers

### Setup

- Create `.env` file contents
```env
DATABASE_USER=""
DATABASE_HOST=""
MYSQL_ROOT_PASSWORD=""
SECRET_KEY=""
```

### Start

- execute `make build`
- execute `make up`
- enjoy at http://localhost:3000/docs

### Prettier

- execute `make lint` to verify that your code is clean
- execute `make format` to reformat it
