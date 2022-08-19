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
        self.subitem = None
        self.processa_itens = False
        
    def processa(self, outro_item):
        if self.subitem is None and outro_item.pode_ser_transformado(self):
            item_transformado = outro_item.transforma(self)
            # item_transformado.x = self.x
            # item_transformado.y = self.y
            self.subitem = item_transformado
            return True
        else:
            return False

    def pode_ser_transformado(self, outro_item):
        return False

    def transforma(self, outro_item):
        '''
        Retorna um novo item, resultado da combinação.
        O novo item substitui o item atual.
        Se retornar None, o item atual é removido.
        Se retornar o próprio item, nada acontece.
        '''
        return self

    def pega(self):
        return None

    def draw(self):
        super().draw()
        if self.subitem is not None:
            self.subitem.x = self.x
            self.subitem.y = self.y
            self.subitem.scale = self.scale
            self.subitem.draw()

class TabuaDeCorte(Item):
    def __init__(self):
        super().__init__('assets/tabua.png')
        self.subitem = None
        self.processa_itens = True
    
    def pega(self):
        item = self.subitem
        self.subitem = None
        return item

class Prato(Item):
    def __init__(self):
        super().__init__('assets/prato.png')
        self.processa_itens = True
     
    def pega(self):
        return self

    def processa(self, outro_item):
        processou = super().processa(outro_item)
        if processou:
            return True
        else:
            if self.subitem is not None:
                types = [type(x) for x in [self.subitem, outro_item]]
                # if types == {AlfaceCortada, TomateCortado}:
                if AlfaceCortada in types and TomateCortado in types:
                    self.subitem = SaladaDeAlfaceComTomate()
                    return True
            
        return False

class Tomate(Item):
    def __init__(self):
        super().__init__('assets/tomate.png')
    
    def pode_ser_transformado(self, processador):
        return isinstance(processador, TabuaDeCorte)

    def transforma(self, outro_item):
        if isinstance(outro_item, TabuaDeCorte):
            return TomateCortado()
        else:
            return self
    
    def pega(self):
        return self

class TomateCortado(Item):
    def __init__(self):
        super().__init__('assets/tomate-cortado.png')

    def pode_ser_transformado(self, processador):
        return isinstance(processador, Prato)

    def pega(self):
        return self

class Alface(Item):
    def __init__(self):
        super().__init__('assets/alface.png')
    
    def pode_ser_transformado(self, processador):
        return isinstance(processador, TabuaDeCorte)

    def transforma(self, outro_item):
        if isinstance(outro_item, TabuaDeCorte):
            return AlfaceCortada()
        else:
            return self
    
    def pega(self):
        return self

class AlfaceCortada(Item):
    def __init__(self):
        super().__init__('assets/alface-cortada.png')

    def pode_ser_transformado(self, processador):
        return isinstance(processador, Prato)

    def pega(self):
        return self

class SaladaDeAlfaceComTomate(Item):
    def __init__(self):
        super().__init__('assets/salada-alface-tomate.png')

    def pode_ser_transformado(self, processador):
        return isinstance(processador, Prato)

    def pega(self):
        return self
