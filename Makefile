up:
	docker build ./jupyterlab -t jupyterlab
	docker compose up -d --build

down:
	docker compose down -v
	docker volume rm $(docker volume ls -f name=jupyterhub-user -q)
