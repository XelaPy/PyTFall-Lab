init -1 python:
    # GUI Logic ---------------------------------------------------------------------------------------------
    # One func:
    def point_in_poly(poly, x, y):
    
        n = len(poly)
        inside = False
    
        p1x, p1y = poly[0]
        for i in range(n+1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x, p1y = p2x, p2y
    
        return inside
    
        
    class GuiGirlsList(_object):
        """
        Used for sorting girls in the list and maybe in profile screen in the future
        """
        STATUS_GROUP = 'status'
        OCCUPATION_GROUP = 'occupation'
        ACTION_GROUP = 'action'
        BUILDING_GROUP = 'building'

        def __init__(self):
            self.sorted = list(girl for girl in hero.girls if girl.action != "Exploring")
            self.init_display_filters()
            self.init_active_filters()
            
            self.page = 0
            self.total_pages = 1

        def init_display_filters(self):
            self.display_filters = [
                ('Status', [
                    ['Free', self.STATUS_GROUP, 'free'],
                    ['Slaves', self.STATUS_GROUP, 'slave'],
                    ["Run away", self.ACTION_GROUP, RunawayManager.ACTION] # Put here as "status" makes more sense then "job"
                ]),
                ('Current job', [
                    ['None', self.ACTION_GROUP, None],
                    ['Whore', self.ACTION_GROUP, 'Whore'],
                    ['Guard', self.ACTION_GROUP, 'Guard'],
                    ['Service Girl', self.ACTION_GROUP, 'ServiceGirl'],
                ]),
                ('Courses', [
                    [course_name, self.ACTION_GROUP, course_action] for course_name, course_action in get_all_courses()
                ]),
                ('Occupation', [
                    ['Prostitutes', self.OCCUPATION_GROUP, traits['Prostitute']],
                    ['Strippers', self.OCCUPATION_GROUP, traits['Stripper']],
                    ['Warriors', self.OCCUPATION_GROUP, 'Warrior'],
                    ['Service Girls', self.OCCUPATION_GROUP, 'Server'],
                ]),
                ('Buildings', [
                    [building.name, self.BUILDING_GROUP, building] for building in list(b for b in hero.buildings if b.__class__ != Apartment)
                ]),
            ]

        def init_active_filters(self):
            self.active_filters = {
                self.STATUS_GROUP: set(),
                self.OCCUPATION_GROUP: set(),
                self.BUILDING_GROUP: set(),
                self.ACTION_GROUP: set(),
            }

        def clear(self):
            self.sorted = copy.copy(hero.girls)
            self.init_active_filters()
            renpy.restart_interaction()

        def add_filter(self, group, item):
            if item not in self.active_filters[group]:
                self.active_filters[group] = set([item])
            else:
                self.active_filters[group].remove(item)

        def sort_by_status(self, girl_list):
            for status in self.active_filters[self.STATUS_GROUP]:
                girl_list = list(girl for girl in girl_list if girl.status == status)
            return girl_list

        def sort_by_occupation(self, girl_list):
            for occupation in self.active_filters[self.OCCUPATION_GROUP]:
                girl_list = list(girl for girl in girl_list if occupation in girl.occupations)
            return girl_list

        def sort_by_action(self, girl_list):
            for action in self.active_filters[self.ACTION_GROUP]:
                girl_list = list(girl for girl in girl_list if girl.action == action)
            return girl_list

        def sort_by_brothel(self, girl_list):
            for building in self.active_filters[self.BUILDING_GROUP]:
                girl_list = list(girl for girl in girl_list if girl.location == building)
            return girl_list

        def get_sorted(self):
            return self.sort_by_brothel(
                self.sort_by_occupation(
                    self.sort_by_action(
                        self.sort_by_status(self.sorted)
                    )
                )
            )

        def get_focus(self, filter_group, filter_key):
            return filter_key in self.active_filters[filter_group]

        
    
    class GuiHeroProfile(_object):
        '''The idea is to try and turn the while loop into the function
        I want girl_meets and quests to work in similar way
        This is basically practicing :)
        '''
        def __init__(self):
            self.show_item_info = False
            self.item = False
            
            self.finance_filter = "day"
            self.came_from = None # To enable jumping back to where we originally came from.

        def show_unequip_button(self):
            if self.item and self.item in hero.eqslots.values():
                return True
                
        def show_equip_button(self):
            if self.item and self.item.sex != "female" and self.item.id in hero.inventory.content:
                return True
                
                
    class PytGallery(_object):
        """
        PyTFall gallery to view girl's pictures and controls
        """
        def __init__(self, char):
            self.girl = char
            self.default_imgsize = (960, 660)
            self.imgsize = self.default_imgsize
            self.tag = "profile"
            self.tagsdict = tagdb.get_tags_per_character(self.girl)
            self.td_mode = "full" # Tagsdict Mode (full or dev)
            self.pathlist = list(tagdb.get_imgset_with_all_tags(set([char.id, "profile"])))
            self.imagepath = self.pathlist[0]
            self._image = self.pathlist[0]
            self.tags = " | ".join([i for i in tagdb.get_tags_per_path(self.imagepath)])
        
        def screen_loop(self):
            while 1:
                result = ui.interact()
                
                if result[0] == "image":
                    index = self.pathlist.index(self.imagepath)
                    if result[1] == "next":
                        index = (index + 1) % len(self.pathlist)
                        self.imagepath = self.pathlist[index]
                        self.set_img()

                    elif result[1] == "previous":
                        index = (index - 1) % len(self.pathlist)
                        self.imagepath = self.pathlist[index]
                        self.set_img()
                    
                elif result[0] == "tag":
                    self.tag = result[1]
                    self.pathlist = list(tagdb.get_imgset_with_all_tags(set([self.girl.id, result[1]])))
                    self.imagepath = self.pathlist[0]                  
                    self.set_img()
                    
                elif result[0] == "view_trans":
                    gallery.trans_view()
                    
                # This is for the testing option (only in dev mode):
                elif result[0] == "change_dict":
                    if result[1] == "full":
                        self.td_mode = "full"
                        self.tagsdict = tagdb.get_tags_per_character(self.girl)
                    elif result[1] == "dev":
                        self.td_mode = "dev"
                        d = tagdb.get_tags_per_character(self.girl)
                        self.tagsdict = OrderedDict()
                        for i in d:
                            if i in ["portrait", "vnsprite", "battle_sprite"]:
                                self.tagsdict[i] = d[i]
                        
                elif result[0] == "control":
                    if result[1] == 'return':
                        break
                   
        @property
        def image(self):
            return ProportionalScale("/".join([self.girl.path_to_imgfolder, self._image]), self.imgsize[0], self.imgsize[1])
                        
        def set_img(self):
            if self.tag in ("vnsprite", "battle_sprite"):
                self.imgsize = self.girl.get_sprite_size(self.tag)
            else:
                self.imgsize = self.imgsize
                
            self._image = self.imagepath
            self.tags = " | ".join([i for i in tagdb.get_tags_per_path(self.imagepath)])
                
                
        def trans_view(self):
            """
            I want to try and create some form of automated transitions/pics loading for viewing mechanism.
            Transitions are taken from Ceramic Hearts.
            """
            # Get the list of files for transitions first:
            transitions = list()
            path = content_path("gfx/masks")
            for file in os.listdir(path):
                if file.endswith((".png", ".jpg", ".jpeg")):
                    transitions.append("/".join([path, file]))
            transitions.reverse()
            transitions_copy = copy.copy(transitions)
            
            # Get the images:
            images = self.pathlist * 1
            shuffle(images)
            images_copy = copy.copy(images)
            
            renpy.hide_screen("gallery")
            renpy.with_statement(dissolve)
            
            renpy.show_screen("gallery_trans")
            
            renpy.music.play("content/sfx/music/reflection.mp3", fadein=1.5)
            
            global stop_dis_shit
            stop_dis_shit = False
            
            first_run = True
            
            while not stop_dis_shit:
                
                if not images:
                    images = images_copy * 1
                if not transitions:
                    transitions = transitions_copy * 1
                    
                image = images.pop()
                image = "/".join([self.girl.path_to_imgfolder, image])
                x, y = renpy.image_size(image)
                rndm = randint(5, 7)
                if first_run:
                    first_run = False
                else:
                    renpy.hide(tag)
                tag = str(random.random())
                
                if x > y:
                    ratio = config.screen_height/float(y)
                    if int(round(x * ratio)) <= config.screen_width:
                        image = ProportionalScale(image, config.screen_width, config.screen_height)
                        renpy.show(tag, what=image, at_list=[truecenter, simple_zoom_from_to_with_linear(1.0, 1.5, rndm)])
                        renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                        renpy.pause(rndm-3)
                    else:
                        image = ProportionalScale(image, 10000, config.screen_height)
                        renpy.show(tag, what=image, at_list=[move_from_to_align_with_linear((0.0, 0.5), (1.0, 0.5), rndm)])
                        renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                        renpy.pause(rndm-3)
                elif y > x:
                    ratio = 1366/float(x)
                    if int(round(y * ratio)) <= 768:
                        image = ProportionalScale(image, config.screen_width, config.screen_height)
                        renpy.show(tag, what=image, at_list=[truecenter, simple_zoom_from_to_with_linear(1.0, 1.5, rndm)])
                        renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                        renpy.pause(rndm-3)
                    else:    
                        image = ProportionalScale(image, config.screen_width, 10000)
                        renpy.show(tag, what=image, at_list=[truecenter, move_from_to_align_with_linear((0.5, 1.0), (0.5, 0.0), rndm)])
                        renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                        renpy.pause(rndm-3)
                else:
                    image = ProportionalScale(image, config.screen_width, config.screen_height)
                    renpy.show(tag, what=image, at_list=[truecenter, simple_zoom_from_to_with_linear(1.0, 1.5, rndm)])
                    renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                    renpy.pause(rndm-3)
                    
                    
                    
            renpy.hide_screen("gallery_trans")
            renpy.music.stop(fadeout=1.0)
            renpy.hide(tag)
            renpy.show_screen("gallery")
            renpy.with_statement(dissolve)
