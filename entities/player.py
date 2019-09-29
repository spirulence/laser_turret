import pyglet


class Player(object):
    def __init__(self, image_path, position, move_keys):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image(image_path))
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2
        self.sprite.rotation = 90
        self.sprite.position = position
        self.up_key, self.left_key, self.down_key, self.right_key = move_keys
        self.alive = True
        self.faces_collected = 0
        self.is_collidable = True

    def update(self, state):
        if self.alive:
            if state.keys[self.right_key]:
                self.sprite.x += 4
            if state.keys[self.left_key]:
                self.sprite.x -= 4
            if state.keys[self.up_key]:
                self.sprite.y += 4
            if state.keys[self.down_key]:
                self.sprite.y -= 4

    def draw(self):
        if self.alive:
            self.sprite.draw()