import pyglet


class Laser(object):
    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('laser_line.png'))
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2
        self.sprite.x = 1920/2
        self.sprite.y = 1080/2
        self.alive = False
        self.is_collidable = False

    def update(self, state):
        state.laser_time -= 1
        self.alive = state.laser_time > 0
        self.sprite.rotation = state.laser_rotation

    def draw(self):
        if self.alive:
            self.sprite.draw()