import pyglet

class Scoreboard():
    def __init__(self):
        self.label = pyglet.text.HTMLLabel(
            '0', x=0, y=0,
            anchor_x='center', anchor_y='center')
        self.label.color = (255, 255, 255, 255)
        self.is_collidable = False
    
    def update(self, string, x, y):
        self.label = pyglet.text.HTMLLabel(
            string,
            x=x, y=y,
            anchor_x='center', anchor_y='center')
        self.label.color = (255, 255, 255, 255)

    def draw(self):
        self.label.draw()