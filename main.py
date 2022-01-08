from accounts_info.menu import account_menu

list_len = 5

def main():
    items = ({"data_load": "re-load", "menu_option": "menu", "alter_list": list_len, 
        "message_opt": "no", "message": ' ', "list_len": list_len})
    account_menu(items)
    
if __name__ == "__main__":
    # execute only if run as a script
    main()    
    
    
