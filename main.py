import math
import random

import pyglet
from pyglet.window import key

from entities.cover import Cover
from entities.gameendgraphic import GameEndGraphic
from entities.laser import Laser
from entities.laserturret import LaserTurret
from entities.player import Player

pyglet.resource.path += ["resources"]

window = pyglet.window.Window(width=1920, height=1080, fullscreen=True)

pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)


class collision(object):
    def __init__(self, entity1, entity2):
        self.entity1 = entity1
        self.entity2 = entity2

def get_collisions(e1, entities):
    collisions = []
    e1.collisions = []
    for e2 in entities:
        if e2.is_collidable and e1 is not e2 and abs(e1.sprite.x - e2.sprite.x) < 20 and abs(e1.sprite.y - e2.sprite.y) < 20:
            coll = collision(e1, e2)
            collisions.append(coll)
    return collisions

class Consumable():
    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('resources/smiley.png'))
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2
        self.sprite.x = 1920/2
        self.sprite.y = 1080/2
        self.consumed = False
        self.is_collidable = True

    def update(self, state):
        pass

    def draw(self):
        if not self.consumed:
            self.sprite.draw()

    def consume(player):
        player.score += 1

# class Scoreboard():
#     def __init__(self):
#         self.label = pyglet.text.HTMLLabel(
#             '<font face="Times New Roman" size="4">Hello, <i>world</i></font>',
#             x=window.width//2, y=window.height//2,
#             anchor_x='center', anchor_y='center')


player_1 = Player('player_1.png', (200, 540), (key.W, key.A, key.S, key.D))
player_2 = Player('player_2.png', (1720, 540), (key.I, key.J, key.K, key.L))

entities = [
    player_1, player_2, LaserTurret(), Laser()
]

cover = []

for i in range(15):
    x, y = random.randrange(1920), random.randrange(1080)
    if math.isclose(x, 1920/2, abs_tol=200) and math.isclose(y, 1080/2, abs_tol=200):
        pass
    else:
        cover.append(Cover(x, y))

entities += cover

player_1_wins = GameEndGraphic('player_1_wins.png')
player_2_wins = GameEndGraphic('player_2_wins.png')
turret_wins = GameEndGraphic('turret_wins.png')

keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)


class GlobalState(object):

    def __init__(self, cover):
        self.keys = keys
        self.laser_rotation = None
        self.laser_time = 0
        self.cover = cover

    @staticmethod
    def laser_collision(entity, laser_rotation):
        laser_rotation = (-laser_rotation + 90) % 360
        rotation_radians = math.atan2(entity.sprite.y - 1080 / 2, entity.sprite.x - 1920 / 2)
        rotation_degrees = math.degrees(rotation_radians) % 360
        return math.isclose(rotation_degrees, laser_rotation, abs_tol=3)

    @staticmethod
    def distance_from_center(entity):
        return math.hypot(entity.sprite.x - 1920/2, entity.sprite.y - 1080/2)

    def fire_laser(self, rotation):
        fired_upon = []

        for cover in self.cover:
            if self.laser_collision(cover, rotation) and cover.alive:
                fired_upon.append(cover)

        for player in [player_1, player_2]:
            if self.laser_collision(player, rotation) and player.alive:
                fired_upon.append(player)

        fired_upon.sort(key=lambda entity: self.distance_from_center(entity))

        if fired_upon:
            fired_upon[0].alive = False

        self.laser_time = 5
        self.laser_rotation = rotation


state = GlobalState(cover)


def on_draw(time_delta):
    for e in entities:
        e.update(state)

    window.clear()

    if not (player_1.alive or player_2.alive):
        turret_wins.draw()
    elif player_1.faces_collected >= 10:
        player_1_wins.draw()
    elif player_2.faces_collected >= 10:
        player_2_wins.draw()
    else:
        for e in entities:
            e.draw()


pyglet.clock.schedule(on_draw)
pyglet.app.run()
