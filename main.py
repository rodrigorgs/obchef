import pyglet

class MainWindow(pyglet.window.Window):
  def __init__(self):
    super(MainWindow, self).__init__(960, 540, resizable=False)
    self.cozinha = Cozinha()

  def on_draw(self):
    self.clear()
    self.cozinha.draw()

  def on_key_press(self, symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        pyglet.app.exit()
    self.cozinha.on_key_press(symbol, modifiers)

class Tilemap:
    def __init__(self, width, height, tile_size, origin_x, origin_y):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.tiles = []
        for l in range(self.height):
            self.tiles.append([None] * self.width)

    def set_tile(self, x, y, tile):
        self.tiles[y][x] = tile
        if tile is not None:
            tile.x, tile.y = self.map_to_screen(x, y)
    
    def get_tile(self, x, y):
        return self.tiles[y][x]
    
    def map_to_screen(self, map_x, map_y):
        screen_x = self.origin_x + map_x * self.tile_size
        screen_y = self.origin_y + (self.height - map_y - 1) * self.tile_size
        return screen_x, screen_y
    
    def screen_to_map(self, screen_x, screen_y):
        map_x = (screen_x - self.origin_x) // self.tile_size
        map_y = self.height - 1 - (screen_y - self.origin_y) // self.tile_size
        return map_x, map_y
    
    def draw(self):
        for l in range(self.height):
            for c in range(self.width):
                tile = self.get_tile(c, l)
                if tile:
                    tile.draw()

class Cozinha:
    TILE_SIZE = 60

    def __init__(self):
        self.tilemap = Tilemap(16, 8, self.TILE_SIZE, 0, 60)
        self.objetos = Tilemap(16, 8, self.TILE_SIZE, 0, 60)

        mapa = [
            '****************',
            '*       *      *',
            '*       ***    *',
            '*              *',
            '*              *',
            '*       *      *',
            '*       *      *',
            '****************',
        ]
        self.configura_mapa(self.tilemap, mapa)
        objetos = [
            '  PP            ',
            '                ',
            'T        T      ',
            '                ',
            't               ',
            '                ',
            '                ',
            '                ',
        ]
        self.configura_mapa(self.objetos, objetos)
        
        self.cozinheiro = Cozinheiro(self, 1, 1)

    def configura_mapa(self, tilemap, mapa):
        mapa = [list(linha) for linha in mapa]
        for l in range(len(mapa)):
            linha = mapa[l]
            for c in range(len(linha)):
                if linha[c] == '*':
                    tilemap.set_tile(c, l, Mesa())
                elif linha[c] == 'T':
                    tilemap.set_tile(c, l, TabuaDeCorte())
                elif linha[c] == 't':
                    tilemap.set_tile(c, l, Tomate())
                elif linha[c] == 'P':
                    tilemap.set_tile(c, l, Prato())

    # TODO: mover para cozinheiro
    def on_key_press(self, symbol, modifiers):
        dx, dy = 0, 0
        if symbol == pyglet.window.key.UP:
            dy -= 1
        elif symbol == pyglet.window.key.DOWN:
            dy += 1
        elif symbol == pyglet.window.key.LEFT:
            dx -= 1
        elif symbol == pyglet.window.key.RIGHT:
            dx += 1
        
        print('move', dx, dy)
        self.cozinheiro.move(dx, dy)

        if symbol == pyglet.window.key.SPACE:
            self.cozinheiro.interage()

    def eh_caminhavel(self, x, y):
        return self.tilemap.get_tile(x, y) is None

    def draw(self):
        self.tilemap.draw()
        self.objetos.draw()
        self.cozinheiro.draw()

class Cozinheiro(pyglet.sprite.Sprite):
    def __init__(self, cozinha, map_x=0, map_y=0):
        # super().__init__(pyglet.resource.image('assets/cozinheiro-cima.png'), x, y)
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('assets/cozinheiro-cima.png'), 0, 0)
        self.cozinha = cozinha
        self.map_x = map_x
        self.map_y = map_y
        self.dx = 0
        self.dy = -1
        self.objeto_pego = None
        self.atualiza_sprite()
    
    @property
    def target_x(self):
        return self.map_x + self.dx

    @property
    def target_y(self):
        return self.map_y + self.dy

    def move(self, dx, dy):
        if dx != 0 or dy != 0:
            self.olha_para(dx, dy)

            if self.cozinha.eh_caminhavel(self.map_x + dx, self.map_y + dy):
                self.map_x = self.map_x + dx
                self.map_y = self.map_y + dy

                self.atualiza_sprite()

    def atualiza_sprite(self):
        screen_x, screen_y = self.cozinha.tilemap.map_to_screen(self.map_x, self.map_y)
        self.sprite.x = screen_x
        self.sprite.y = screen_y

    def interage(self):
        if self.objeto_pego is None:
            self.pega_prato()
        else:
            self.larga_prato()

    def larga_prato(self):
        # TODO: verifica se tem espaço para largar o prato
        if self.objeto_pego is not None:
            self.objeto_pego.scale = 1
            self.cozinha.objetos.set_tile(self.target_x, self.target_y, self.objeto_pego)
            self.objeto_pego = None

    def pega_prato(self):
        prato = self.cozinha.objetos.get_tile(self.target_x, self.target_y)
        if isinstance(prato, Prato):
            self.objeto_pego = prato
            self.cozinha.objetos.set_tile(self.target_x, self.target_y, None)
            prato.scale = 0.5
    
    def draw(self):
        self.sprite.draw()
        if self.objeto_pego is not None:
            screen_x, screen_y = self.cozinha.objetos.map_to_screen(self.target_x, self.target_y)
            self.objeto_pego.x = screen_x + self.cozinha.TILE_SIZE / 4
            self.objeto_pego.y = screen_y + self.cozinha.TILE_SIZE / 4
            self.objeto_pego.draw()
    
    def olha_para(self, x, y):
        self.dx = x
        self.dy = y
        if x == 1:
            self.sprite.image = pyglet.resource.image('assets/cozinheiro-direita.png')
        elif x == -1:
            self.sprite.image = pyglet.resource.image('assets/cozinheiro-esquerda.png')
        elif y == -1:
            self.sprite.image = pyglet.resource.image('assets/cozinheiro-cima.png')
        else:
            self.sprite.image = pyglet.resource.image('assets/cozinheiro-baixo.png')

class Chao(pyglet.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__(pyglet.resource.image('assets/chao.png'), x, y)

class Mesa(pyglet.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__(pyglet.resource.image('assets/mesa.png'), x, y)

class TabuaDeCorte(pyglet.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__(pyglet.resource.image('assets/tabua.png'), x, y)

class Prato(pyglet.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__(pyglet.resource.image('assets/prato.png'), x, y)

class Tomate(pyglet.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__(pyglet.resource.image('assets/tomate.png'), x, y)


if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()