build:
	docker compose build

up:
	docker compose up -d api

down:
	docker compose down

lint:
	docker run --rm --volume ./:/src --workdir /src pyfound/black:latest_release black --check .

format:
	docker run --rm --volume ./:/src --workdir /src pyfound/black:latest_release black .

shell:
	docker compose up -d api && \
	docker compose exec -it api bash

logs:
	docker compose logs -f api
