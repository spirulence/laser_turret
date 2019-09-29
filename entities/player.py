import math

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

    def laser_collision(self, laser_rotation):
        laser_rotation = (-laser_rotation + 90) % 360
        rotation_radians = math.atan2(self.sprite.y - 1080 / 2, self.sprite.x - 1920 / 2)
        rotation_degrees = math.degrees(rotation_radians) % 360
        return math.isclose(rotation_degrees, laser_rotation, abs_tol=3)

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

        if state.laser_time > 0 and self.laser_collision(state.laser_rotation):
            self.alive = False

    def draw(self):
        if self.alive:
            self.sprite.draw()