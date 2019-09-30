import math
import random

import pyglet
from pyglet.window import key

from entities.gameendgraphic import GameEndGraphic
from entities.laser import Laser
from entities.laserturret import LaserTurret
from entities.player import Player
from entities.consumable import Consumable

pyglet.resource.path += ["resources"]

window = pyglet.window.Window(width=1920, height=1080, fullscreen=True)

pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

player_1 = Player('player_1.png', (200, 540), (key.W, key.A, key.S, key.D))
player_2 = Player('player_2.png', (1720, 540), (key.I, key.J, key.K, key.L))

entities = [
    player_1, player_2, LaserTurret(), Laser()
]

for x in range(20):
    entities.append(Consumable(random.random()*1920, random.random()*1080))

player_1_wins = GameEndGraphic('player_1_wins.png')
player_2_wins = GameEndGraphic('player_2_wins.png')
turret_wins = GameEndGraphic('turret_wins.png')

keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)


class GlobalState(object):

    def __init__(self):
        self.keys = keys
        self.laser_rotation = None
        self.laser_time = 0

    def set_laser(self, rotation):
        self.laser_rotation = rotation
        self.laser_time = 4


state = GlobalState()


def on_draw(time_delta):
    for e in entities:
        e.update(state , entities)

    window.clear()

    if not (player_1.alive or player_2.alive):
        turret_wins.draw()
    elif player_1.score >= 10:
        player_1_wins.draw()
    elif player_2.score >= 10:
        player_2_wins.draw()
    else:
        for e in entities:
            e.draw()


pyglet.clock.schedule(on_draw)
pyglet.app.run()
