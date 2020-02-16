16th Feb 2020
============
$ docker-compose -f docker-compose.prod.yml build
$ docker-compose -f docker-compose.prod.yml up -d
$ docker exec -it btreProd_container bash
$ python3 runserver 0.0.0.0:8000

At web-browser: localhost:1337
