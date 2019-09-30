import pyglet
from pyglet.window import key


class LaserTurret(object):
    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('turret.png'))
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2
        self.sprite.x = 1920/2
        self.sprite.y = 1080/2
        self.cooldown_time = 180
        self.cooldown_elapsed = 60
        self.is_collidable = True

    def update(self, state, entities):
        self.cooldown_elapsed += 1

        if state.keys[key.V]:
            self.sprite.rotation += 1
        if state.keys[key.B]:
            self.sprite.rotation -= 1
        if state.keys[key.SPACE] and self.cooldown_elapsed >= self.cooldown_time:
            state.set_laser(self.sprite.rotation)
            self.cooldown_elapsed = 0

    def draw(self):
        self.sprite.draw()