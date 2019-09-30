import math

import pyglet

from entities.scoreboard import Scoreboard
from entities.consumable import Consumable

class collision(object):
    def __init__(self, entity1, entity2):
        self.entity1 = entity1
        self.entity2 = entity2

def get_collisions(e1, entities):
    collisions = []
    e1.collisions = []
    for e2 in entities:
        if e2.is_collidable and e1 is not e2 and abs(e1.sprite.x - e2.sprite.x) < 40 and abs(e1.sprite.y - e2.sprite.y) < 40:
            coll = collision(e1, e2)
            collisions.append(coll)
    return collisions

class Player(object):
    def __init__(self, image_path, position, move_keys):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image(image_path))
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2
        self.sprite.rotation = 90
        self.sprite.position = position
        self.up_key, self.left_key, self.down_key, self.right_key = move_keys
        self.alive = True
        self.score = 0
        self.is_collidable = True
        self.scoreboard = Scoreboard()

    def laser_collision(self, laser_rotation):
        laser_rotation = (-laser_rotation + 90) % 360
        rotation_radians = math.atan2(self.sprite.y - 1080 / 2, self.sprite.x - 1920 / 2)
        rotation_degrees = math.degrees(rotation_radians) % 360
        return math.isclose(rotation_degrees, laser_rotation, abs_tol=3)

    def update(self, state, entities):
        if self.alive:
            if state.keys[self.right_key]:
                self.sprite.x += 4
            if state.keys[self.left_key]:
                self.sprite.x -= 4
            if state.keys[self.up_key]:
                self.sprite.y += 4
            if state.keys[self.down_key]:
                self.sprite.y -= 4
            self.scoreboard.label.x = self.sprite.x
            self.scoreboard.label.y = self.sprite.y + 40

        if state.laser_time > 0 and self.laser_collision(state.laser_rotation):
            self.alive = False

        collisions = get_collisions(self, entities)
        for c in collisions:
            if isinstance(c.entity2, Consumable) and c.entity2.alive:
                c.entity2.consume(self)

    def draw(self):
        if self.alive:
            self.sprite.draw()
            self.scoreboard.label.draw()