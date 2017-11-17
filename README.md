hacksoft.io
==============================
[ ![Codeship Status for HackSoftware/hacksoft.io](https://app.codeship.com/projects/72dbbc50-7ce3-0135-5c44-361f0802280c/status?branch=master)](https://app.codeship.com/projects/245780)

A HackSoft website based on the wagtail CMS. It is deployed here: www.hacksoft.io

## Local development setup

The project is using:

-   Python 3.6.2
-   Django 1.10

In order to setup it, there are the following steps:

### Install OS requirements (Linux only)

```bash
$ ./utility/install_os_dependencies.sh
```

### Install Python requirements

```bash
$ pip install -r requirements/local.txt
```

### Setup Postgres

Linux:

```bash
$ sudo -u postgres createuser your_postgres_username
$ sudo -u postgres createdb -O your_postgres_username hacksoft
```

Mac OSX:

```bash
$ createuser your_postgres_username
$ createdb -O your_postgres_username hacksoft
```

To run migrations
```bash
$ python manage.py migrate
```

### Bootstrap data

At this point you have working server with empty database. Since it's a CMS the content of the site is inside your database. To fetch latest production database backup you'll have to do the following:

* Setup `heroku-cli` and login. See https://devcenter.heroku.com/articles/heroku-cli for more details.

* Give the script permissions and execute it:

```bash
$ chmod +x ./utility/pgrestore_with_latest_production_db.sh
$ ./utility/pgrestore_with_latest_production_db.sh
```

### Compiling sass

In order to compile sass:

```bash
$ sass --watch hacksoft/static/sass/main.scss:hacksoft/static/css/main.css
```

### Tests

There are no tests.
