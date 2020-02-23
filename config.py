# DEFAULT USER CREDENTIALS
default_creds = [
                {  "user_id" : "default",
                    "password" : "default",
                    "root_access" : False,
                    "email_id" : "default@example.com"
                    },
                {   "user_id" : "root",
                    "password" : "root",
                    "root_access" : True,
                    "email_id" : "root@example.com"
                    }]

# PATHS
# path for encryption key
crypt_key_path = "./data/keys"
# path for authentication db
auth_db_path = "./data"