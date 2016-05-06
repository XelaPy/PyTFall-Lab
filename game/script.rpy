
        
    


label start:
    $ menu_extensions = MenuExtension()
    
label menus:
    menu:
        "GFX":
            menu:
                "UDDs":
                    $ pass
                "Screens":
                    while 1:
                        menu:
                            "Quests Pop Up":
                                show screen quest_notifications("Frog Princess", "Starts")
                            "Drag And Drop":
                                call test_drags
                            "Exit":
                                jump start
                            
        "Logic":
            $ pass
