from .tilemap import Tilemap
from .cozinheiro import Cozinheiro
from .itens import *
import pyglet

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
        
        self.cozinheiro.move(dx, dy)

        if symbol == pyglet.window.key.SPACE:
            self.cozinheiro.interage()

    def eh_caminhavel(self, x, y):
        return self.tilemap.get_tile(x, y) is None

    def draw(self):
        self.tilemap.draw()
        self.objetos.draw()
        self.cozinheiro.draw()
