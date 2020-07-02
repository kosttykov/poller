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
sudo docker-compose up
```

Quit the server


Run:

```
docker-compose run web python manage.py migrate --noinput
```

```
docker-compose run web python manage.py collectstatic --no-input --clear
```

Then you can run conatiners in daemon mode:

```
docker-compose up -d
```

Also you can create superuser:

```
docker-compose run web python manage.py createsuperuser
```