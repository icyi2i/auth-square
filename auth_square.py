################################################################################
#   Author  	-   Sarthak Gambhir
#   Description -   User management module for authentication and CRUD
#					functionality over basic credentials!
################################################################################

from sqlite3 import connect
from cryptography import fernet as crypt
from os import makedirs
import config

class user_auth():
	crypt_key_path = config.crypt_key_path + "/crypt_key_file"
	auth_db_path = config.auth_db_path + "/auth.db"
	default_creds = config.default_creds

	def __init__(self):
		pass
		# print("auth_square - to simplify and separate user management from the app")
		# print(self.default_creds)
		# print(self.crypt_key_path)
		# print(self.auth_db_path)

	# Resets the database to removing old credentials and revert root user to default
	def setup(self):
		operation_status = self.__crypt_key_gen()
		if operation_status:
			try:
				with open(self.crypt_key_path) as crypt_key_file:
					cipher = crypt.Fernet(crypt_key_file.read())
				con = connect(self.auth_db_path)
				cur = con.cursor()
				cur.execute("DROP TABLE IF EXISTS auth")
				cur.execute("""CREATE TABLE IF NOT EXISTS auth (user_id TEXT PRIMARY KEY NOT NULL,
																password TEXT NOT NULL,
																root_access BOOLEAN NOT NULL,
																email_id TEXT UNIQUE NOT NULL)""")
				cur.execute(	"INSERT INTO auth VALUES (?,?,?,?)",
								(	self.default_creds["user_id"],
									cipher.encrypt(bytes(self.default_creds["password"], "UTF-8")).decode(),
									self.default_creds["root_access"],
									self.default_creds["email_id"]
									)
								)
				con.commit()
				con.close()
				operation_status = True
			except:
				operation_status = False
		return operation_status

	# ONLY CALLED IN THE SETUP! MAY USE IT TO BLOCK A USER BY EMAIL IN THE FUTURE!
	# Generate a new encryption key to deprecate old passwords
	def __crypt_key_gen(self):
		try:
			crypt_key = crypt.Fernet.generate_key()
			makedirs("/".join(self.crypt_key_path.split("/")[:-1]), exist_ok=True)
			with open(self.crypt_key_path, "w") as crypt_key_file:
				crypt_key_file.write(str(crypt_key, "UTF-8"))
			operation_status = True
		except:
			operation_status = False
		return operation_status

	# Returns auth information of all the users
	def view_all_users(self):
		try:
			con = connect(self.auth_db_path)
			cur = con.cursor()
			cur.execute("SELECT user_id, root_access, email_id FROM auth")
			user_data = cur.fetchall()
			con.close()
			return user_data
		except:
			return None 
	
	# Authenticate a user with "user_id" and "password"
	def authenticate_user(self, user_id, password):
		auth_status = False
		try:	
			with open(self.crypt_key_path) as crypt_key_file:
				cipher = crypt.Fernet(crypt_key_file.read())
			
			con = connect(self.auth_db_path)
			cur = con.cursor()
			cur.execute("SELECT password FROM auth WHERE user_id = ?", (user_id,))
			# print(cipher.decrypt(bytes(cur.fetchone()[0], "UTF-8")).decode())
			if password == str(cipher.decrypt(bytes(cur.fetchone()[0], "UTF-8")).decode()):
				auth_status = True
			con.close()
		except:
			pass
		return auth_status

	# Change user password
	def change_password(self, user_id, old_password, new_password):
		status = False
		try:
			with open(self.crypt_key_path) as crypt_key_file:
				cipher = crypt.Fernet(crypt_key_file.read())
			
			con = connect(self.auth_db_path)
			cur = con.cursor()
			cur.execute("SELECT password FROM auth WHERE user_id = ?", (user_id,))
			# print(cipher.decrypt(bytes(cur.fetchone()[0], "UTF-8")).decode())
			if old_password == str(cipher.decrypt(bytes(cur.fetchone()[0], "UTF-8")).decode()):
				cur.execute("UPDATE auth set password = ? WHERE user_id = ?", (cipher.encrypt(bytes(new_password, "UTF-8")).decode(), user_id))
				status = True
			con.commit()
			con.close()
		except:
			pass
		return status

	# Create new user
	def create_user(self, user_id, password, root_access, email_id):
		status = False
		try:
			with open(self.crypt_key_path) as crypt_key_file:
				cipher = crypt.Fernet(crypt_key_file.read())
			
			con = connect(self.auth_db_path)
			cur = con.cursor()
			cur.execute("INSERT INTO auth VALUES (?,?,?,?)", (user_id, cipher.encrypt(bytes(password, "UTF-8")).decode(), root_access, email_id))
			status = True
			con.commit()
			con.close()
		except:
			pass
		return status

	# Delete a user	
	def delete_user(self, user_id, password):
		status = False
		try:
			with open(self.crypt_key_path) as crypt_key_file:
				cipher = crypt.Fernet(crypt_key_file.read())
			
			con = connect(self.auth_db_path)
			cur = con.cursor()
			cur.execute("SELECT password FROM auth WHERE user_id = ?", (user_id,))
			if password == str(cipher.decrypt(bytes(cur.fetchone()[0], "UTF-8")).decode()):
				cur.execute("DELETE FROM auth WHERE user_id = ?", (user_id,))
				status = True
			con.commit()
			con.close()
		except:
			pass
		return status