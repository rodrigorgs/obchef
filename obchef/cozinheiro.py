from .itens import *
import pyglet

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
            self._pega_item()
        else:
            self._larga_item()

    def _larga_item(self):
        # TODO: verifica se tem espaço para largar o prato
        
        # tomate na tabua: tomate.combina(tabua) => tomate cortado
        # tomate no prato: tomate.pode_combinar(prato) => False

        # tomate cortado no prato
        # prato no tomate cortado
        
        item = self.objeto_pego
        outro_item = self.cozinha.objetos.get_tile(self.target_x, self.target_y)
        
        if outro_item is None:
            self.objeto_pego.scale = 1
            self.objeto_pego = None
            self.cozinha.objetos.set_tile(self.target_x, self.target_y, item)
        else:
            items = [item, outro_item]
            processadores = [x for x in items if x.processa_itens]
            if len(processadores) == 1:
                processador = processadores[0]
                a_processar = [x for x in items if x is not processador][0]

                if processador.processa(a_processar):
                    self.objeto_pego.scale = 1
                    self.objeto_pego = None
                    novo = processador.transforma(a_processar)
                    self.cozinha.objetos.set_tile(self.target_x, self.target_y, novo)

    def _pega_item(self):
        item = self.cozinha.objetos.get_tile(self.target_x, self.target_y)
        item_obtido = item.pega()
        if item_obtido is not None:
            self.objeto_pego = item_obtido
            if item_obtido is item:
                self.cozinha.objetos.set_tile(self.target_x, self.target_y, None)
            item_obtido.scale = 0.5
    
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
