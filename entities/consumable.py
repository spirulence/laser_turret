import pyglet

class Consumable():
    def __init__(self, x, y):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('resources/happy_face.png'))
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2
        self.sprite.x = x
        self.sprite.y = y
        self.alive = True
        self.is_collidable = True

    def update(self, state, entities):
        pass

    def draw(self):
        if self.alive:
            self.sprite.draw()

    def consume(self, player):
        self.alive = False
        player.score += 1
        player.scoreboard.update(str(player.score), player.sprite.x, player.sprite.y)