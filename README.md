# Superclimbing_application_project

Superclimbing application is a catalog application that provides a list of items within a variety of climbing categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Requirements
* Python versions (2.x or 3.x).
* Flask [http://flask.pocoo.org/docs/0.12/installation/]
* Flask_seasurf (SeaSurf is a Flask extension for preventing cross-site request forgery (CSRF).)[http://flask-seasurf.readthedocs.io/en/latest/]
* Flask_uploads (Flask-Uploads allows your application to flexibly and efficiently handle file uploading and serving the uploaded files. )      [https://pythonhosted.org/Flask-Uploads/]
* Postgresql [https://www.postgresql.org/download/]
* VirtualBox [https://www.virtualbox.org/wiki/Download_Old_Builds_5_1]
* Vagrant [https://www.vagrantup.com/]

## Install
--------
1. Clone the template project, replacing my-project with the name of the project you are creating:
```
git clone https://github.com/PaulinaMoreno/superclimbing_app_catalog.git my-project
cd my-project
```
2. Create the *superclimbing* database:
   1. Go to the catalog directory and type:
      ```
       python models.py
      ```
      this will setup the models required for the database.
   2. in the same directory type :
       ```
         python insert_info.py
       ```
       this will populate the database with categories and items data. The *superclimbing.db* database will be created in the catalog directory

3. The application works with Google Oauth, you need to follow the next steps :
    1. Go to your app's page in the Google APIs Console — https://console.developers.google.com/apis
    2. Choose Credentials from the menu on the left.
    3. Create an OAuth Client ID.
    4. This will require you to configure the consent screen, with the same choices as in the video.
    5. When you're presented with a list of application types, choose Web application. You can then set the authorized JavaScript origins,
    with the same settings as in the video.
    6. You will then be able to get the client ID and client secret. You can also download the client secret as a JSON data file once you have created it.
    7. You need to copy the client secret JSON file to catalog directory as: *client_secret*
    8. You need to go to superclimbing.py file and change the *SECRET_KEY* value with the  *client_secret* value in the *client_secret.json* file:
                          ```
                          app.config['SECRET_KEY'] = "client_secret"
                          ```

4. Run superclimbing.py file :
  ```
    python superclimbing.py
  ```
After this step the application will be running in *localhost:8000/superclimbing*
## Contributing
------------
Find any typos? Have more ideas of questions the reporting tool could answer? Contributions are welcome!

First, fork this repository.

![Fork Icon](images/fork-icon.png)

Next, clone this repository to your desktop to make changes.

```sh
$ git clone {YOUR_REPOSITORY_CLONE_URL}
```

Once you've pushed changes to your local repository, you can issue a pull request by clicking on the green pull request icon.

![Pull Request Icon](images/pull-request-icon.png)


Authors
----------------
* ***Paulina Moreno***
