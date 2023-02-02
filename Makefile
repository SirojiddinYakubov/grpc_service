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

help:
	@echo "make"
	@echo "    hello"
	@echo "        print hello world"

hello:
	echo "Hello, World"
run-test:
	pytest -c course_svc/pytest.ini
run-server:
	export PYTHONPATH=$$PWD/course_svc/app:$$PYTHONPATH; cd course_svc && python app/server.py
run-docker-build:
	docker-compose -f docker-compose-dev.yml build
run-docker-up:
	docker-compose -f docker-compose-dev.yml up --build
run-pgadmin:
	docker-compose -f pgadmin.yml up --build
