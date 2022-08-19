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