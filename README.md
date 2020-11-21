```
╋╋╋╋╋╋╋╋┏┓ ┏┓
╋╋╋╋╋╋╋╋┃┃ ┃┃
┏━━┓┏━━┓┃┃ ┃┃ ┏━━┓┏━┓
┃┏┓┃┃┏┓┃┃┃ ┃┃ ┃┃━┫┃┏┛
┃┗┛┃┃┗┛┃┃┗┓┃┗┓┃┃━┫┃┃
┃┏━┛┗━━┛┗━┛┗━┛┗━━┛┗┛
┃┃
┗┛
```

<h3>

* Python/Django
* PostgreSQL
* Docker
* Nginx

</h3>

<br>

<h1>
Installing Docker:
</h1>

```
sudo apt-get install docker docker-compose
```

<h1>
Building and configuring images:
</h1>

Go to the project directory

<br>

Build images:
```
sudo docker-compose build
```

Run in daemon mode:
```
sudo docker-compose up -d
```
*project will run on 127.0.0.1:1337

<br>

Make migrations:
```
sudo docker-compose exec web python manage.py makemigrations
```
```
sudo docker-compose exec web python manage.py migrate 
```

Collect static:
```
sudo docker-compose exec web python manage.py collectstatic --noinput --clear
```

Restart containers:
```
sudo docker-compose restart
```

Also you need to create a superuser:
```
sudo docker-compose exec web python manage.py createsuperuser
```
