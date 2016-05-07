
        
    


label start:
    $ menu_extensions = MenuExtension()
    
label menus:
    menu:
        "GFX":
            menu:
                "UDDs":
                    while 1:
                        menu:
                            "Shooting Range":
                                call shooting_range
                            "Exit":
                                jump start
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
