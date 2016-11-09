HackSoft Wagtail
==============================
A HackSoft website based on the wagtail CMS. It is deployed here: www.hacksoft.io


## Basic Commands

### Setting Up Your Users

* To create a **normal user account**, just go to Sign Up and fill out the form. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Running tests
This is a simple website with basically no functionallity. There are no tests.


### Deployment
The system is hosted on kyup.com. If your key is on our publickey repo you shoud have access to the server. 

```
$ ssh root@hacksoft.io
```

Don`t change the setup. The VPS is provisioned by ansible script located in bitbucket.

**Deployment:**
You can deploy the master to production using our ansible tower.
http://tower.hacksoft.io/

