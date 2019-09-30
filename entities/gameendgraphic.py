import pyglet


class GameEndGraphic(object):
    def __init__(self, image_path):
        sprite = pyglet.sprite.Sprite(img=pyglet.resource.image(image_path))
        sprite.image.anchor_x = sprite.image.width / 2
        sprite.image.anchor_y = sprite.image.height / 2
        sprite.x = 1920 / 2
        sprite.y = 1080 / 2

        self.sprite = sprite

    def update(self, _state):
        pass

    def draw(self):
        self.sprite.draw()