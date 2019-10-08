from auth_square import user_auth

auth = user_auth()

choice = None
menu_separator = "="*64

while True:
    print("\n" + menu_separator)
    print("Choose operation :")
    print("1 - View all users")
    print("2 - Create new user")
    print("3 - Change password")
    print("4 - Delete existing user")
    print("5 - Authenticate user")
    print("6 - Exit")
    print("0 - Auth-square Setup (Reset)")
    print(menu_separator + "\n")
    
    try:
        choice = int(input("Enter your choice : "))
    except ValueError:
        choice = -1

    if choice == 0:
        print(auth.setup())
    elif choice == 1:
        print(auth.view_all_users())
    elif choice == 2:
        print(auth.create_user(input("USERNAME - "), input("PASSWORD - "), True if input("ROOT ACCESS(y/n) - ") == "y" else False, input("EMAIL - ")))
    elif choice == 3:
        print(auth.change_password(input("USERNAME - "), input("OLD PASSWORD - "), input("NEW PASSWORD - ")))
    elif choice == 4:
        print(auth.delete_user(input("USERNAME - "), input("PASSWORD - ")))
    elif choice == 5:
        print(auth.authenticate_user(input("USERNAME - "), input("PASSWORD - ")))
    elif choice == 6:
        exit(0)
    else:
        print("Invalid Choice! Try again.")
