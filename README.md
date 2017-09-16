hacksoft.io
==============================
[ ![Codeship Status for HackSoftware/hacksoft.io](https://app.codeship.com/projects/72dbbc50-7ce3-0135-5c44-361f0802280c/status?branch=master)](https://app.codeship.com/projects/245780)

A HackSoft website based on the wagtail CMS. It is deployed here: www.hacksoft.io

## Basic Commands

### Compiling sass

In order to compile sass:

```bash
$ sass --watch hacksoft/static/sass/main.scss:hacksoft/static/css/main.css
```

### Running tests

This is a simple website with basically no functionallity. There are no tests.


### Deployment

The system is hosted on [kyup.com](https://kyup.com/). If your key is on our publickey repo you shoud have access to the server. 

```
$ ssh root@hacksoft.io
```

Don not change the setup. The VPS is provisioned by ansible script located in a private repo.
