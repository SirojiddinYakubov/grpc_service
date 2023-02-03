#!/usr/bin/make

include .env

define SERVERS_JSON
{
	"Servers": {
		"1": {
			"Name": "course-svc",
			"Group": "Servers",
			"Host": "$(DATABASE_HOST)",
			"Port": 5432,
			"MaintenanceDB": "postgres",
			"Username": "$(DATABASE_PASSWORD)",
			"SSLMode": "prefer",
			"PassFile": "/tmp/pgpassfile"
		}
	}
}
endef
export SERVERS_JSON
export PYTHONPATH=:$(PWD)/course_svc/app
help:
	@echo "make"
	@echo "    hello"
	@echo "        print hello world"

hello:
	echo "Hello, World"
test:
	pytest -s -c course_svc/pytest.ini
run:
	cd course_svc && python app/server.py
docker-build:
	docker-compose -f docker-compose-dev.yml build
docker-up:
	docker-compose -f docker-compose-dev.yml up --build
pgadmin:
	docker-compose -f pgadmin.yml up --build
proto:
	cd course_svc/app && python -m grpc_tools.protoc -I protos --python_out=grpc_generated_files --grpc_python_out=grpc_generated_files protos/*.proto
