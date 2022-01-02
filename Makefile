setting: 
	chmod -R 755 ./scripts
	./scripts/set.sh

clean:
	./scripts/clean.sh

analysis:
	./scripts/analyze.sh

build:
	docker-compose up -d --build --force-recreate

locust:
	(cd data_source_mock && poetry run locust --config=locust.conf)