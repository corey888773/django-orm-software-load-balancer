.PHONY:
	postgres down ubuild ustart

postgres:
	docker run --name postgres-lb1  -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=todo -p 5432:5432 -d postgres:latest

down:
	docker-compose down --remove-orphans --rmi all

ubuild:
	docker-compose up --build --remove-orphans

ustart:
	docker-compose up --remove-orphans