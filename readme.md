# CS235Flix Web Application

## Description

A Web application that demonstrates use of Python's Flask framework. The application makes use of libraries such as the Jinja templating library and WTForms. Architectural design patterns and principles including Repository and Single Responsibility have been used to design the application. The application uses Flask Blueprints to maintain a separation of concerns between application functions. The application makes use of ORM database using SQLAlchemy. Testing includes unit and end-to-end testing using the pytest tool. 

## Installation

**Installation via requirements.txt**

```shell
$ cd CS235Flix_web_app
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:COMPSCI-235' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *CS235Flix_web_app_sqldb* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 


## Configuration

The */.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.
* `SQLALCHEMY_DATABASE_URI`: Relative location of the database (for file based `sqlite:///csflix235.db`, for memory based `sqlite://`).
* `REPOSITORY`: Sets the mode of the application (should be `database`), (`memory` may be used for testing new features).


## Testing

Testing requires that file */tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the */tests/data* directory. 

E.g. 

`TEST_DATA_PATH = os.path.join("C:", os.sep, "Users", "Michael", "OneDrive", "Documents", "UoA", "COMPSCI_235", "Assignment_3", "CS235Flix_web_app_sqldb", "test", "data")`

assigns TEST_DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

`C:\Users\Michael\OneDrive\Documents\UoA\COMPSCI_235\Assignment_3\CS235Flix_web_app_sqldb\test\data`

You can then run tests from within PyCharm.

 