```
╋╋╋╋╋╋┏┓┏┓
╋╋╋╋╋╋┃┃┃┃
┏━━┳━━┫┃┃┃┏━━┳━┓
┃┏┓┃┏┓┃┃┃┃┃┃━┫┏┛
┃┗┛┃┗┛┃┗┫┗┫┃━┫┃
┃┏━┻━━┻━┻━┻━━┻┛
┃┃
┗┛
```

<hr>

<h1>
Installation:
</h1>

```
sudo apt-get install docker docker-compose
```

<h1>
Launch:
</h1>

Go to the project directory

Run:

```
sudo docker-compose build
```

```
sudo docker-compose up -d
```

Run:

```
sudo docker-compose exec web python manage.py migrate --noinput
```

```
sudo docker-compose exec web python manage.py collectstatic --no-input --clear
```

Also you can create superuser:

```
sudo docker-compose exec web python manage.py createsuperuser
```
