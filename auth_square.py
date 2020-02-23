################################################################################
#   Author  	-   Sarthak Gambhir
#   Description -   User management module for authentication and CRUD
#					functionality over basic user credentials!
################################################################################

# IMPORTING MODULES
import sqlite3 as db
from cryptography import fernet as crypt
from os import makedirs

# CONFIGURATION FROM config.py
import config

# MAIN AUTHENTICATION CLASS
class user_auth():
	# CONFIGURATION VARIABLES
	crypt_key_path = config.crypt_key_path + "/crypt_key_file"
	auth_db_path = config.auth_db_path + "/auth.db"
	default_creds = config.default_creds

	# EVERYTIME YOU INITIALIZE THIS CLASS
	def __init__(self):
		# print("auth_square - To simplify and separate user management from applications!")
		pass

	# ONLY CALLED IN THE SETUP! DO NOT LEAVE ENDPOINTS FOR THIS
	# RESET DATABASE WITH DEFAULT CREDENTIALS
	def __reset_database__(self):
		# READ ENCRYPTION KEY
		with open(self.crypt_key_path) as crypt_key_file:
			cipher = crypt.Fernet(crypt_key_file.read())
		# CONNECT TO DATABASE
		con = db.connect(self.auth_db_path)
		cur = con.cursor()
		# DROP PREVIOUS TABLE, CREATE NEW TABLE, & CREATE DEFAULT USERS' ENTRIES
		cur.execute("DROP TABLE IF EXISTS auth")
		cur.execute("""CREATE TABLE IF NOT EXISTS auth (user_id TEXT PRIMARY KEY NOT NULL,
														password TEXT NOT NULL,
														root_access BOOLEAN NOT NULL,
														email_id TEXT UNIQUE NOT NULL)""")
		for default_cred in self.default_creds:
			cur.execute("INSERT INTO auth VALUES (?,?,?,?)",
			(	default_cred["user_id"],
				cipher.encrypt(bytes(default_cred["password"], "UTF-8")).decode(),
				default_cred["root_access"],
				default_cred["email_id"]
				))
		# COMMIT TO AND CLOSE THE DATABASE
		con.commit()
		con.close()
	
	# ONLY CALLED IN THE SETUP! MAY USE IT TO BLOCK A USER BY EMAIL IN THE FUTURE!
	# GENERATE A NEW ENCRYPTION KEY TO DEPRECATE OLD PASSWORDS
	def __crypt_key_gen__(self):
		operation_data = {"operation_status" : False, "operation_message" : None}
		try:
			# Generate key
			crypt_key = crypt.Fernet.generate_key()
			# Make directory path
			makedirs(config.crypt_key_path, exist_ok=True)
			# WRITE TO KEY FILE
			with open(self.crypt_key_path, "w") as crypt_key_file:
				crypt_key_file.write(str(crypt_key, "UTF-8"))
			# SUCCESSFULLY GENERATED NEW ENCRYPTION KEY
			operation_data["operation_status"] = True
			operation_data["operation_message"] = "Info : New encryption key generated successfully!"
		except Exception as e:
			# FAILED GENERATION OF NEW ENCRYPTION KEY
			operation_data["operation_status"] = False
			operation_data["operation_message"] = "Error : {0}".format(str(e))
		return operation_data

	# RESETS THE DATABASE TO REMOVE ALL OLD CREDENTIALS AND GENERATE DEFAULT USER
	# YOU MAY NOT WANT TO GIVE USERS ACCESS TO THIS
	def setup(self):
		# GENERATE NEW ENCRYPTION KEY
		operation_data = self.__crypt_key_gen__()
		# CHECK IF KEY GENERATED SUCCESSFULLY
		if operation_data["operation_status"]:
			try:
				self.__reset_database__()
				operation_data["operation_status"] = True
				operation_data["operation_message"] = "Info : Database reset successful! Default user created!"
			except Exception as e:
				# ANY EXCEPTION WILL LEAD TO OPERATION BEING ABORTED
				# NO DATABASE COMMITS WILL BE DONE (Control does not reach there)
				operation_data["operation_status"] = False
				operation_data["operation_message"] = "Error : {0}".format(str(e))
		return operation_data

	# RETURNS DETAILS OF ALL USERS ELSE "None"
	def get_all_users(self, root_id = None, root_pw = None):
		operation_data = {"users" : None, "operation_message" : "", "operation_status" : False}
		try:
			auth_data = self.authenticate_user(root_id, root_pw)
			if auth_data["auth_status"]:
				if auth_data["root_access"]:
					# CONNECT TO DATABASE
					con = db.connect(self.auth_db_path)
					con.row_factory = db.Row

					cur = con.cursor()
					# GET PASSWORD FROM THE TABLE
					# SELECT ALL DETAILS EXCEPT PASSWORD FROM TABLE
					cur.execute("SELECT user_id, root_access, email_id FROM auth")
					operation_data["users"] = [dict(x) for x in cur.fetchall()]
					con.close()
					operation_data["operation_message"] = "Info : USER DATA READ SUCCESSFULLY!"
					operation_data["operation_status"] = True
				else:
					operation_data["operation_message"] = "Error : User '{0}' does not have root access!".format(root_id)
			else:
				operation_data["operation_message"] = auth_data["operation_message"]
		except Exception as e:
			operation_data["operation_message"] = "Error : {0}".format(str(e))
		return operation_data

	# AYTHENTICATES A USER WITH "user_id" & "password", AND RETURNS STATUS
	def authenticate_user(self, user_id = None, password = None):
		# DEFAULT STATUS RESPONSE
		auth_data = {"auth_status" : False, "root_access" : False, "operation_message" : ""}
		try:
			if user_id == None:
				auth_data["operation_message"] = "Error : User ID can not be None! Check function call."
			elif password == None:
				auth_data["operation_message"] = "Error : Password can not be None! Check function call."
			else:
				# READ ENCRYPTION KEY
				with open(self.crypt_key_path) as crypt_key_file:
					cipher = crypt.Fernet(crypt_key_file.read())
				# CONNECT TO DATABASE
				con = db.connect(self.auth_db_path)
				cur = con.cursor()
				# GET PASSWORD FROM THE TABLE
				cur.execute("SELECT password, root_access FROM auth WHERE user_id = ?", (user_id,))
				query_data = cur.fetchone()
				# DECRYPT AND COMPARE PASSWORDS
				if password == str(cipher.decrypt(bytes(query_data[0], "UTF-8")).decode()):
					# PASSWORDS MATCHED
					auth_data["auth_status"] = True
					auth_data["operation_message"] = "Info : Authentication successful!"
					auth_data["root_access"] = bool(query_data[1])
				else:
					auth_data["operation_message"] = "Error : Authentication failed! Passwords did not match."
				con.close()
		except TypeError:
			auth_data["operation_message"] = "Error : Authentication failed! User '{0}' does not exist.".format(user_id)
		except Exception as e:
			auth_data["operation_message"] = "Error : {0}".format(str(e))
		return auth_data

	# CREATE NEW USER (does not require root level permission)
	def create_user(self, user_id = None, password = None, root_access = False, email_id = None):
		# DEFAULT STATUS RESPONSE
		operation_data = {"operation_status" : False, "operation_message" : ""}
		try:
			if user_id == None:
				operation_data["operation_message"] = "Error : User ID can not be None! Check function call."
			elif password == None:
				operation_data["operation_message"] = "Error : Password can not be None! Check function call."
			else:
				# READ ENCRYPTION KEY
				with open(self.crypt_key_path) as crypt_key_file:
					cipher = crypt.Fernet(crypt_key_file.read())
				# CONNECT TO DATABASE
				con = db.connect(self.auth_db_path)
				cur = con.cursor()
				# CHECK IF USER ID OR EMAIL ID IS ALREADY USED
				user_id_taken = cur.execute("SELECT * FROM auth WHERE user_id == ?", (user_id,)).fetchone()
				email_id_taken = cur.execute("SELECT * FROM auth WHERE email_id == ?", (email_id,)).fetchone()
				if user_id_taken:
					operation_data["operation_message"] = "Error : This User ID is taken. Choose another ID."
				elif email_id_taken:
					operation_data["operation_message"] = "Error : This email ID is taken. Contact admin if you don't own that account or choose another."
				else:
					# CREATE USER
					cur.execute("INSERT INTO auth VALUES (?,?,?,?)", (user_id, cipher.encrypt(bytes(password, "UTF-8")).decode(), root_access, email_id))
					# SUCCESSFULLY CREATED THE USER
					operation_data["operation_message"] = "Info : Successfully created new user!"
					operation_data["operation_status"] = True
				
				# COMMIT TO AND CLOSE THE DATABASE
				con.commit()
				con.close()
		except db.Error as e:
			print(e)
			operation_data["operation_message"] = "Error : {0}".format(str(e))
		return operation_data

	# CHANGE PASSWORD AS USER USING OLD PASSWORD
	def change_password_as_user(self, user_id = None, old_password = None, new_password = None):
		# DEFAULT STATUS RESPONSE
		operation_data = {"operation_status" : False, "operation_message" : ""}
		try:
			if user_id == None:
				operation_data["operation_message"] = "Error : User ID can not be None! Check function call."
			elif old_password == None:
				operation_data["operation_message"] = "Error : Old password can not be None! Check function call."
			elif new_password == None:
				operation_data["operation_message"] = "Error : New password can not be None! Check function call."
			else:
				# READ ENCRYPTION KEY
				with open(self.crypt_key_path) as crypt_key_file:
					cipher = crypt.Fernet(crypt_key_file.read())
				# CONNECT TO DATABASE
				con = db.connect(self.auth_db_path)
				cur = con.cursor()
				
				# AUTHENTICATE USER WITH OLD PASSWORD
				auth_data = self.authenticate_user(user_id = user_id, password = old_password)
				if auth_data["auth_status"]:
					# CHANGE PASSWORD
					cur.execute("UPDATE auth set password = ? WHERE user_id = ?", (cipher.encrypt(bytes(new_password, "UTF-8")).decode(), user_id))
					# PASSWORD CHANGED
					operation_data["operation_status"] = True
					operation_data["operation_message"] = "Info : Password changed successfully!"
				else:
					operation_data["operation_message"] = auth_data["operation_message"]
				# COMMIT TO AND CLOSE THE DATABASE
				con.commit()
				con.close()
		except Exception as e:
			operation_data["operation_message"] = "Error : {0}".format(str(e))
		return operation_data

	# CHANGE PASSWORD AS A ROOT USER
	def change_password_as_root(self, root_id = None, root_pw = None, user_id = None, new_password = None):
		# DEFAULT STATUS RESPONSE
		operation_data = {"operation_status" : False, "operation_message" : ""}
		try:
			if root_id == None:
				operation_data["operation_message"] = "Error : Root ID can not be None! Check function call."
			elif root_pw == None:
				operation_data["operation_message"] = "Error : Root password can not be None! Check function call."
			elif user_id == None:
				operation_data["operation_message"] = "Error : User ID can not be None! Check function call."
			elif new_password == None:
				operation_data["operation_message"] = "Error : New user password can not be None! Check function call."
			else:
				# READ ENCRYPTION KEY
				with open(self.crypt_key_path) as crypt_key_file:
					cipher = crypt.Fernet(crypt_key_file.read())
				# CONNECT TO DATABASE
				con = db.connect(self.auth_db_path)
				cur = con.cursor()
				
				# AUTHENTICATE ROOT USER
				auth_data = self.authenticate_user(user_id = root_id, password = root_pw)
				if auth_data["auth_status"]:
					if auth_data["root_access"]:
						user_exists = cur.execute("SELECT * FROM auth WHERE user_id == ?", (user_id,)).fetchone()
						if user_exists:
							# CHANGE PASSWORD
							cur.execute("UPDATE auth set password = ? WHERE user_id = ?", (cipher.encrypt(bytes(new_password, "UTF-8")).decode(), user_id))
							# PASSWORD CHANGED
							operation_data["operation_status"] = True
							operation_data["operation_message"] = "Info : Password changed successfully!"
						else:
							operation_data["operation_message"] = "Error : User '{0}' does not exist!".format(user_id)
					else:
						operation_data["operation_message"] = "Error : User '{0}' does not have root access!".format(root_id)
				else:
					operation_data["operation_message"] = auth_data["operation_message"]
				# COMMIT TO AND CLOSE THE DATABASE
				con.commit()
				con.close()
		except Exception as e:
			operation_data["operation_message"] = "Error : {0}".format(str(e))
		return operation_data

	# DELETE PROFILE AS USER
	def delete_profile_as_user(self, user_id = None, password = None):
		operation_data = {"operation_status" : False, "operation_message" : ""}
		try:
			if user_id == None:
				operation_data["message"] = "Error : User ID can not be None! Check function call."
			elif password == None:
				operation_data["operation_message"] = "Error : Password can not be None! Check function call."
			else:
				# AUTHENTICATE USER
				auth_data = self.authenticate_user(user_id = user_id, password = password)
				if auth_data["auth_status"]:
					# CONNECT TO DATABASE
					con = db.connect(self.auth_db_path)
					cur = con.cursor()
					# DELETE USER
					cur.execute("DELETE FROM auth WHERE user_id = ?", (user_id,))
					# SUCCESSFULLY DELETED THE USER
					operation_data["operation_message"] = "Info : User deleted successfuly!"
					operation_data["operation_status"] = True
				else:
					operation_data["operation_message"] = auth_data["operation_message"]
				# COMMIT TO AND CLOSE THE DATABASE
				con.commit()
				con.close()
		except Exception as e:
			operation_data["operation_message"] = "Error : {0}".format(str(e))
		return operation_data

	# DELETE PROFILE AS ROOT
	def delete_profile_as_root(self, root_id = None, root_pw = None, user_id = None):
		operation_data = {"operation_status" : False, "operation_message" : ""}
		try:
			if root_id == None:
				operation_data["operation_message"] = "Error : Root ID can not be None! Check function call."
			elif root_pw == None:
				operation_data["operation_message"] = "Error : Root password can not be None! Check function call."
			elif user_id == None:
				operation_data["operation_message"] = "Error : User ID to be deleted can not be None! Check function call."
			else:
				# AUTHENTICATE ROOT
				auth_data = self.authenticate_user(user_id = root_id, password = root_pw)
				if auth_data["auth_status"]:
					# CONNECT TO DATABASE
					con = db.connect(self.auth_db_path)
					cur = con.cursor()
					# DELETE USER
					cur.execute("DELETE FROM auth WHERE user_id = ?", (user_id,))
					# SUCCESSFULLY DELETED THE USER
					operation_data["operation_message"] = "Info : User deleted successfuly!"
					operation_data["operation_status"] = True
				else:
					operation_data["operation_message"] = auth_data["operation_message"]
				# COMMIT TO AND CLOSE THE DATABASE
				con.commit()
				con.close()
		except Exception as e:
			operation_data["operation_message"] = "Error : {0}".format(str(e))
		return operation_data