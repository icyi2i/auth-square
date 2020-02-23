# Auth-square
A minimal user management module for cryptography based authentication and CRUD functionality over unique email/user id and password as credentials!

## Getting started
Auth-square is a python 3 module which you can import in your program and stop worrying about authentication of users. It uses **cryptography** module for password encryption which you can install using the command.

```
pip install cryptography
```

## Usage
To use this module -
- Place the __auth_sqaure__ and __config__ scripts in the root folder of your app.
- In your app, import the main **user_auth** class, using the following statement. Create an instance of it.

```
from auth_square import user_auth
auth = user_auth()
```

- After object creation, you can call its methods to perform the available operations

You can also check the example script "example_admin_app.py" for reference.

### Changing default paths

You can change paths of your database file and encryption key in the __config__ script under:
```
# PATHS
# path for encryption key
crypt_key_path = "./data/keys"
# path for authentication db
auth_db_path = "./data"
```
Make sure to either:
- run setup after changing this path to generate new database and key

or
- move your previous database and key file folder to the new location  

### Methods

The following public methods are available for the class:

- setup

	Resets and initializes the authentication database file with default credentials and ***removes all previous user credentials***.

	The default credentials can be changed in config file under [default_creds]

	```
	# DEFAULT USER CREDENTIALS
	default_creds = [	{  "user_id" : "default",
							"password" : "default",
							"root_access" : False,
							"email_id" : "default@example.com"
							},
						{   "user_id" : "root",
							"password" : "root",
							"root_access" : True,
							"email_id" : "root@example.com"
							}]
	```

	Returns a dictionary with operation status and operation message.

	> **Warning** : Do not add access to this method to your main application unless you know what you are doing or want admin controls.

- view_all_users

	Returns opeartion status, operation message, and all users' details except password as a list of dictionaries. The details consists of user_id, root_access, and email_id.
	
- authenticate_user

	Checks authentication of user by comparing the credentials from the database. This method takes two arguments as:

	```
	auth.authenticate(user_id, password);
	```

	The response consists of boolean authentication status, boolean root access, and operation message.

- create_user

	Create a new user by passing all the credentials as:

	```
	auth.create_user(user_id, password, root_access, email_id)
	```
	The return value is dictionary containing boolean operation status, and operation message.

- change_password_as_user

	This method allows a user to change his/her password by passing the arguments as:

	```
	auth.change_password(user_id, old_password, new_password)
	```
	The return value is dictionary containing boolean operation status, and operation message.

- change_password_as_root

	This method allows a root user to change somebody else's password in admin mode by passing the arguments as:

	```
	auth.change_password(root_id, root_pw, user_id, new_password)
	```
	The return value is dictionary containing boolean operation status, and operation message.

- delete_profile_as_user

	Deletes a user after authenticating with the credentials as:

	```
	auth.delete_user(user_id, password)
	```
	The return value is dictionary containing boolean operation status, and operation message.

- delete_profile_as_root

	This method allows a root user to delete another user after authenticating with the credentials as:

	```
	auth.delete_user(root_id, root_pw,)
	```
	The return value is dictionary containing boolean operation status, and operation message.

## Built with

[Cryptography - Github page](https://github.com/pyca/cryptography)

## Author

Sarthak Gambhir - <a href="https://github.com/icyi2i">Github profile</a>

## License
This project is licensed under the MIT License - see the LICENSE.md file for details