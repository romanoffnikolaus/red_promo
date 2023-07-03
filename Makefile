make run:
	python manage.py runserver

make admin:
	python manage.py createsuperuser

make migrate:
	python manage.py makemigrations
	python manage.py migrate

make static:
	python manage.py collectstatic

make test:
	python manage.py test

make up:
	sudo docker-compose up

make down:
	sudo docker-compose down
	
