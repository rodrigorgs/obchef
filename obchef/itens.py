import pyglet

class Chao(pyglet.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__(pyglet.resource.image('assets/chao.png'), x, y)

class Mesa(pyglet.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__(pyglet.resource.image('assets/mesa.png'), x, y)

############

class Item(pyglet.sprite.Sprite):
    def __init__(self, filename):
        super().__init__(pyglet.resource.image(filename), 0, 0)

class TabuaDeCorte(Item):
    def __init__(self):
        super().__init__('assets/tabua.png')

class Prato(Item):
    def __init__(self):
        super().__init__('assets/prato.png')

class Tomate(Item):
    def __init__(self):
        super().__init__('assets/tomate.png')
