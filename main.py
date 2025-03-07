import pygame as pg, sys

pg.init()

scr = pg.display.set_mode((800, 800))

class Puzzle:
    def __init__(self, sprite_path: str, image_size: tuple[int] = (800, 800), cell_size: int = 100):
        self.full_sprite = pg.image.load(sprite_path).convert_alpha()
        self.cell_size = cell_size
        self.image_size = image_size
        self.individual_sprite = {
            (i * cell_size, j * cell_size): self.full_sprite.subsurface((i * cell_size, j * cell_size, cell_size, cell_size))
            for i in range(self.image_size[0] // self.cell_size)
            for j in range(self.image_size[1] // self.cell_size)
        }

    def render(self, surf: pg.Surface): 
        for pos, sprite in self.individual_sprite.items():
            surf.blit(sprite, pos)
        for i in range(self.image_size[0] // self.cell_size):
            for j in range(self.image_size[1] // self.cell_size):
                pg.draw.rect(surf, (0, 0, 0), (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size), 1)
def main():

    puzzle = Puzzle("images/charizard.png")

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()

        scr.fill((0, 0, 0))
        puzzle.render(scr)
        pg.display.flip()

if __name__ == "__main__": main()