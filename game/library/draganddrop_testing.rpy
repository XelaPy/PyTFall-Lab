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
                    self.pos.append(x, y)
                    y = y + size[1] + yspacing
                
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
            
        # Get an item
        # Items coordinates: page number * page size + displacement from the start of the current page
        def getitem(self, i):
            return self.content[self.page * self.page_size + i]
            
        # group of methods realizing the interface of common listing
        # remove and add an element
        # with recalc of current page
        def add(self, item):
            if item not in self.content:
                self.content.append(item)

        def remove(self, item):
            if item in self.content:
                self.content.remove(item)
                

