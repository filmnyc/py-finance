from accounts_info.menu import account_menu

def main():
    items = ({"data_load": "re-load", "menu_option": "menu", "alter_list": 5, 
        "message_opt": "no", "message": ' '})
    account_menu(items)
    
if __name__ == "__main__":
    # execute only if run as a script
    main()    
    
    
