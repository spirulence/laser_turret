import math

import pyglet
from pyglet.window import key

window = pyglet.window.Window(width=1920, height=1080, fullscreen=True)

pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)


def player_angle_to_laser(player_position):
    rotation_radians = math.atan2(player_position[1] - 1080 / 2, player_position[0] - 1920 / 2)
    rotation_degrees = math.degrees(rotation_radians)
    return rotation_degrees % 360


# print((0, 0), player_angle_to_laser((0, 0)))
# print((1920, 0), player_angle_to_laser((1920, 0)))
# print((0, 1080), player_angle_to_laser((0, 1080)))
# print((1920, 1080), player_angle_to_laser((1920, 1080)))


def laser_collision(player_position, laser_rotation):
    laser_rotation = (-laser_rotation + 90) % 360
    rotation_radians = math.atan2(player_position[1] - 1080/2, player_position[0] - 1920/2)
    rotation_degrees = math.degrees(rotation_radians) % 360
    return math.isclose(rotation_degrees, laser_rotation, abs_tol=3)

# assert laser_collision((0,0), -128)
# assert laser_collision((1920,0), 126)
# assert laser_collision((0,1080), -59)
# assert laser_collision((1920,1080), 51)

class PlayerOne(object):

    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('resources/player_1.png'))
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2
        self.sprite.rotation = 90
        self.sprite.x = 0
        self.sprite.y = 0
        self.alive = True

    def update(self, state):
        if self.alive:
            if state.keys[key.D]:
                self.sprite.x += 4
            if state.keys[key.A]:
                self.sprite.x -= 4
            if state.keys[key.W]:
                self.sprite.y += 4
            if state.keys[key.S]:
                self.sprite.y -= 4

        if state.laser_time > 0 and laser_collision(self.sprite.position, state.laser_rotation):
            self.alive = False

    def draw(self):
        if self.alive:
            self.sprite.draw()


class PlayerTwo(object):

    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('resources/player_2.png'))
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2
        self.sprite.rotation = -90
        self.sprite.x = 0
        self.sprite.y = 0
        self.alive = True

    def update(self, state):
        if self.alive:
            if state.keys[key.L]:
                self.sprite.x += 4
            if state.keys[key.J]:
                self.sprite.x -= 4
            if state.keys[key.I]:
                self.sprite.y += 4
            if state.keys[key.K]:
                self.sprite.y -= 4

        if state.laser_time > 0 and laser_collision(self.sprite.position, state.laser_rotation):
            self.alive = False

    def draw(self):
        if self.alive:
            self.sprite.draw()


class LaserTurret(object):

    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('resources/turret.png'))
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2
        self.sprite.x = 1920/2
        self.sprite.y = 1080/2
        self.cooldown_time = 180
        self.cooldown_elapsed = 60

    def update(self, state):
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


class Laser(object):
    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('resources/laser_line.png'))
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2
        self.sprite.x = 1920/2
        self.sprite.y = 1080/2
        self.alive = False

    def update(self, state):
        state.laser_time -= 1
        self.alive = state.laser_time > 0
        self.sprite.rotation = state.laser_rotation

    def draw(self):
        if self.alive:
            self.sprite.draw()


entities = [
    PlayerOne(), PlayerTwo(), LaserTurret(), Laser()
]

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


def on_draw(dt):
    for e in entities: e.update(state)

    window.clear()

    for e in entities: e.draw()


pyglet.clock.schedule(on_draw)
pyglet.app.run()
