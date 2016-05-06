# Drag And Drop testing:

init python:
    class CoordsForPaging(_object):
        """ This class setups up x, y coordinates for items in content list.
        
        We use this in DragAndDrop.
        Might be I'll just use this in the future to handle the whole thing.
        For now, this will be used in combination with screen language.
        *Adaptation of Roman's Inv code!
        """
        def __init__(self, content, columns=2, rows=6, size=(100, 100), xspacing=10, yspacing=10):
            # Should be changes to location in the future:    
            self.content = content
            self.page = 0
            self.page_size = columns*rows

            self.pos = list()
            for c in xrange(columns):
                x = c*size[0]
                if c:
                    x = x + xspacing
                y = 0
                for r in xrange(rows):
                    self.pos.append((x, y))
                    y = y + size[1] + yspacing
                    
        def __len__(self):
            return len(self.content)
            
        def __iter__(self):
            # We return a list of tuples of [(item, pos), (item, pos), ...] for self.page
            page = self.get_page_content()
            pos = self.pos[:len(page)]
            return iter(zip(page, pos))
            
        def __getitem__(self, index):
            # Minding the page we're on!
            return self.content[self.page * self.page_size + index]
            
        def get_pos(self, item):
            # retruns a pos of an item on current page.
            return self.pos[self.get_page_content().index(item)]
            
        def __nonzero__(self):
            return bool(self.content)
                
        # Next page
        def next(self):
            if self.page < self.max_page:
                self.page += 1

        # Previous page
        def prev(self):
            if self.page > 0:
                self.page -= 1
                
        @property
        def max_page(self):
            return len(self.content) / self.page_size if len(self.content) % self.page_size not in [0, self.page_size] else (len(self.content) - 1) / self.page_size
                
        def get_page_content(self):
            start = self.page * self.page_size
            end = (self.page+1) * self.page_size
            return self.content[start:end]
            
        # group of methods realizing the interface of common listing
        # remove and add an element
        # with recalc of current page
        def add(self, item):
            if item not in self.content:
                self.content.append(item)

        def remove(self, item):
            if item in self.content:
                self.content.remove(item)
    
    def fg_dragged(drags, drop):
        x, y = workers.get_pos(drags[0].drag_name)
        
        if not drop:
            drags[0].snap(x, y, delay=0.2)
            renpy.restart_interaction()
            return

        if char.status == "slave":
            drags[0].snap(x, y, delay=0.2)
            renpy.show_screen("message_screen", "Slaves are not allowed to participate in combat!")
            renpy.restart_interaction()
            return

        for team in fg.teams:
            if drop.drag_name == team.name:
                team = team
                break
        else:
            raise Exception, ["Team unknown during drag/drop!", drop.drag_name, team.name]
            
        for t in fg.teams:
            if t and t[0] == char:
                drags[0].snap(x, y, delay=0.2)
                renpy.show_screen("message_screen", "%s is already a leader of %s!" % (char.nickname, t.name))
                renpy.restart_interaction()
                return
            
            if not team:
                for girl in t:
                    if girl == char:
                        drags[0].snap(x, y, delay=0.2)
                        renpy.show_screen("message_screen", "%s cannot lead %s as she's already on %s!" % (char.nickname, team.name, t.name))
                        renpy.restart_interaction()
                        return
                        
        for girl in team:
            if girl == char:
                drags[0].snap(x, y, delay=0.2)
                renpy.show_screen("message_screen", "%s is already on %s!" % (char.nickname, team.name))
                renpy.restart_interaction()
                return
                
        if len(team) == 3:
            drags[0].snap(x, y, delay=0.2)
            renpy.restart_interaction()
            return
        else:
            team.add(char)
            fg_drags.remove(char)
            drags[0].snap(x, y)

        return True
                
                
screen draganddrop():
    fixed:
        pos 100, 100
        for i, pos in workers:
            drag:
                dragged fg_dragged
                drag_name i
                pos pos
                add i
                
label test_drags:
    $ workers = CoordsForPaging(list(Solid("#%06x" % random.randint(0, 0xFFFFFF), xysize=(100, 100)) for i in xrange(50)))
    call screen draganddrop
    return
