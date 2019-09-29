import pyglet


class Cover(object):
    def __init__(self, x, y):
        sprite = pyglet.sprite.Sprite(img=pyglet.resource.image('cover.png'))
        sprite.image.anchor_x = sprite.image.width / 2
        sprite.image.anchor_y = sprite.image.height / 2
        sprite.x = x
        sprite.y = y

        self.sprite = sprite
        self.alive = True

    def update(self, _state):
        pass

    def draw(self):
        if self.alive:
            self.sprite.draw()
