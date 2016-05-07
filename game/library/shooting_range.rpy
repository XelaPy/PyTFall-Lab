transform rmove(d, delay, spos, epos, t):
    d
    subpixel 1
    pause delay
    pos spos
    linear t pos epos
    
transform alphafade(d, delay):
    d
    pause delay
    alpha 1.0
    linear 1.0 alpha .1
    
screen temp_prop_screen(d):
    # Temp screen to display data, should prolly be replaced with classes rendered through UDD in the future.
    add d
    frame:
        align 1.0, 1.0
        has vbox spacing 1
        # fixed:
            # xysize 150, 20
            # text "Hit:" xalign .0
            # text "[d.hit]" xalign 1.0
        # fixed:
            # xysize 150, 20
            # text "Disp:" xalign .0
            # if d.targets:
                # $ x = d.targets[0].xpos
                # $ y = d.targets[0].ypos
                # text "[x], [y]" xalign 1.0 size 14
        # fixed:
            # xysize 150, 20
            # text "Event:" xalign .0
            # text "[d.exp], [d.eyp]" xalign 1.0 size 14
        fixed:
            xysize 150, 20
            text "Ammo:" xalign .0
            text "[d.ammo]" xalign 1.0
        fixed:
            xysize 150, 20
            text "Hits:" xalign .0
            text "[d.hits]" xalign 1.0
        fixed:
            xysize 150, 20
            text "Misses:" xalign .0
            text "[d.misses]" xalign 1.0

    
init python:
    """Simple design for shooting range written in Python/Ren'Py.
    
    What's needed:
    - Can be written as a simple class, UDD, screen or some combination of those. Not yet sure which.
    - Fully contollable animation states for targets.
    - Changing shape of a mouse pointer.
    - Messing with a position of mouse pointer.
    - Showing the weapon? Having that weapon to trace mouse cursor somehow?
    - Input + sounds + special effects but that's the easy part.
    
    - Some cool special feature like seen in some games (zooming in/area scroll/complex sprites/heavy gfx/player damage if targets shoot back... no idea really...)
    """
    
    def get_randomly_colored_solid(size=(100, 100)):
        # Returns a solid of given size and randomized color.
        return Solid("#%06x" % random.randint(0, 0xFFFFFF), xysize=size)
        
    def get_random_target(delay):
        # Returns a transform function with random paramiters to serve as a prop for targets until we have something more real.
        # We move from west to east.
        spos = 20, randint(30, config.screen_height-30) # start pos
        epos = config.screen_width+50, randint(30, config.screen_height-30) # end pos
        t = random.uniform(1.5, 2.7) # time
        size = randint(20, 80), randint(20, 80) # size
        return rmove(get_randomly_colored_solid(size), delay, spos, epos, t), t, size # We need t to know when there is no longer a chance to hit this target.
        
    MBD = pygame.MOUSEBUTTONDOWN
    
    class ShootingRange(renpy.Displayable):
        def __init__(self, **kwargs):

            # Pass additional properties on to the renpy.Displayable
            # constructor.
            super(ShootingRange, self).__init__(**kwargs)
            
            # We add next target at:
            self.next_target = 0
            
            # Transforms:
            self.targets = [] # [transform, childsize, removeat]
            self.gfx = [] # [displayable, removeat]
            
            # Stats:
            self.ammo = 100
            self.hits = 0
            self.misses = 0
            
            # Testing:
            # self.MEOW = 0
            # self.hit = 0
            # self.exp = 0
            # self.eyp = 0

        def render(self, width, height, st, at):
            if not st:
                self.next_target = 0
                self.targets = [] # [transform, childsize, removeat]
                self.gfx = [] # [displayable, removeat]
            
            # remove expired targets:
            for t in self.targets[:]:
                if st >= t[2]:
                    self.targets.remove(t)
                    self.misses = self.misses + 1
                
            if st >= self.next_target:
                target_transform, t, size = get_random_target(st)
                kill = t + st
                self.targets.append([target_transform, size, kill])
                self.next_target = kill + random.uniform(-.75, .25)
                
            render = renpy.Render(config.screen_width, config.screen_height)
            
            for t in self.targets:
                render.place(t[0])
            for gfx in self.gfx[:]:
                if st >= gfx[1]:
                    self.gfx.remove(gfx)
                else:
                    render.place(gfx[0])
                
            renpy.redraw(self, 0)
                
            return render
            
        def check_for_hits(self, x, y):
            # Really simple for now:
            hits = []
            for target in self.targets:
                xs, ys = target[1]
                d = target[0]
                xp, yp = d.xpos, d.ypos
            
                p1 = (xp, yp) # top left
                p2 = (xp+xs, yp) # top right
                p3 = (xp, yp+ys) # bottom left
                p4 = (xp+xs, yp+ys) # bottom right
                p6 = (xp, yp+ys/2) # mid left
                p7 = (xp+xs, yp+ys/2) # mid right
                
                if point_in_poly((p1, p2, p4, p3), x, y):
                    hits.append(target)
            return hits

        def event(self, ev, x, y, st):
            # self.exp = x
            # self.eyp = y
            # if self.targets:
                # self.hit = self.check_for_hits(x, y)
            # renpy.restart_interaction()
            
            if ev.type == MBD:
                if ev.button == 1:
                    self.ammo = self.ammo - 1
                    
                    # play the sound:
                    renpy.music.play("content/sfx/sound/be/Cannon_2.mp3", channel="sound")
                    
                    # check for hits:
                    hit_tragets = self.check_for_hits(x, y)
                    if hit_tragets:
                        for target in hit_tragets:
                            t = target[0]
                            self.gfx.append([alphafade(HitlerKaputt(t.child, 5, pos=(t.xpos, t.ypos)), st), st+1])
                            self.targets.remove(target)
                        self.hits = self.hits + 1
                        self.next_target = st + random.uniform(.1, .4)
                    else:
                        self.misses = self.misses + 1
                        
                    # Update the prop screen.
                    renpy.restart_interaction()
                        
                    if not self.ammo:
                        return "endgame"
                        
        def visit(self):
            return [ ]
        
    def ships_event(ev, x, y, st):
        # Not used atm.
        # A func I wrote for Sprite Manager could of years ago, might come useful for gun sprite if we decide to turn it.
        if ev.type == MOUSEBUTTONDOWN:
            if ev.button == 1:
                if hasattr(store, "ship") and store.ship is not None:
                    ship = store.ship
                    
                    renpy.music.play("picard.wav", channel="sound")
                    
                    angle = math.atan2((y-ship.offset) - ship.show.y, (x-ship.offset) - ship.show.x)
                    angle = angle * (180/math.pi)
                    ship.head = angle + 90
                    
                    ship.target_coords = (x-ship.offset, y-ship.offset)
                    ship.moving = 1
                    renpy.restart_interaction()
                    
                    
label shooting_range:
    scene black
    $ sr = ShootingRange()
    show screen temp_prop_screen(sr)
    python:
        while 1:
            result = ui.interact()
            if result == "endgame":
                break
                
    hide screen temp_prop_screen
    "Hits: [sr.hits], Misses: [sr.misses]"
    "The end..."
    extend " for now :)"
    return
