from auth_square import user_auth
from getpass import getpass
auth = user_auth()

choice = None
menu_separator = "="*80

while True:
    print("\n" + menu_separator)
    print("Choose operation :")
    print("1 - View all users (using root privilege - backend mode)")
    print("2 - Create a non-root user (self - API mode)")
    print("3 - Create a root user")
    print("4 - Change user password (self - API mode)")
    print("5 - Delete user profile (self - API mode)")
    print("6 - Change user password (using root privilege - backend mode)")
    print("7 - Delete user profile (using root privilege - backend mode)")
    print("8 - Authenticate user (self - API mode)")
    print("9 - Exit")
    print("0 - Auth-square Setup")
    print(menu_separator + "\n")

    try:
        choice = int(input("Enter your choice : "))
    except ValueError:
        choice = -1

    if choice == 0:
        print(menu_separator + "\nWARNING - DATABASE WILL BE RESET! TO BE USED IN BACKEND MODE ONLY.\n" + menu_separator)
        if True if input("Do you want to continue? (y/n) : ") == "y" else False:
            print(auth.setup())
        else:
            print("Setup aborted!")
    elif choice == 1:
        print(menu_separator + "\nWARNING - ROOT PRIVELEGE REQUIRED! TO BE USED IN BACKEND MODE ONLY.\n" + menu_separator)
        operation_data = auth.get_all_users(
                                root_id = input("ROOT USER ID : "),
                                root_pw = getpass("ROOT PASSWORD : ")
                            )
        print(operation_data["operation_status"])
        print(operation_data["operation_message"])
        print(operation_data["users"])
    elif choice == 2:
        operation_data = auth.create_user(
                                            user_id =  input("USER ID - "),
                                            password = input("PASSWORD - "),
                                            root_access = False,
                                            email_id = input("EMAIL - ")
                                            )
        print(operation_data["operation_status"])
        print(operation_data["operation_message"])
    elif choice == 3:
        print(menu_separator + "\nWARNING - YOU MIGHT NOT WANT TO GIVE USERS ALL USERS ROOT ACCESS.\n" + menu_separator)
        operation_data = auth.create_user(
                                            user_id =  input("USER ID - "),
                                            password = input("PASSWORD - "),
                                            root_access = True if input("ROOT ACCESS(y/n) - ") == "y" else False,
                                            email_id = input("EMAIL - ")
                                            )
        print(operation_data["operation_status"])
        print(operation_data["operation_message"])
    elif choice == 4:
        operation_data = auth.change_password_as_user(
                user_id = input("USER ID - "),
                old_password = input("OLD PASSWORD - "),
                new_password = input("NEW PASSWORD - ")
                )
        print(operation_data["operation_status"])
        print(operation_data["operation_message"])
    elif choice == 5:
        operation_data = auth.delete_profile_as_user(
                user_id = input("USER ID - "),
                password = getpass("PASSWORD - ")
                )
        print(operation_data["operation_status"])
        print(operation_data["operation_message"])
    elif choice == 6:
        operation_data = auth.change_password_as_root(
                root_id = input("ROOT ID - "),
                root_pw = input("ROOT PASSWORD - "),
                user_id = input("USER ID - "),
                new_password = input("NEW PASSWORD - ")
                )
        print(operation_data["operation_status"])
        print(operation_data["operation_message"])
    elif choice == 7:
        operation_data = auth.delete_profile_as_root(
                root_id = input("ROOT ID - "),
                root_pw = getpass("PASSWORD - "),
                user_id = input("USER ID - ")
                )
        print(operation_data["operation_status"])
        print(operation_data["operation_message"])
    elif choice == 8:
        operation_data = auth.authenticate_user(
                user_id = input("USER ID - "),
                password = getpass("PASSWORD - ")
                )
        print(operation_data["auth_status"])
        print(operation_data["root_access"])
        print(operation_data["operation_message"])
    elif choice == 9:
        exit(0)
    else:
        print("Invalid Choice! Try again.")
