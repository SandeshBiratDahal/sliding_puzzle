import pygame as pg, sys, random

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
        self.individual_sprite_positions = [list(key) for key, item in self.individual_sprite.items()]
        self.individual_sprite_positions.pop(0)
        self.remaining_piece = self.individual_sprite[(0, 0)]
        del self.individual_sprite[(0, 0)]
        self.current_empty_cell = (0, 0)

    def render(self, surf: pg.Surface): 
        i = 0
        for pos, sprite in (self.individual_sprite.items()):
            surf.blit(sprite, self.individual_sprite_positions[i])
            i += 1
        for i in range(self.image_size[0] // self.cell_size):
            for j in range(self.image_size[1] // self.cell_size):
                pg.draw.rect(surf, (0, 0, 0), (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size), 1)

    def check_up(self, x: int, y: int):
        while y >= 0:
            if (x, y) == self.current_empty_cell: return True
            y -= 1
        return False

    def check_down(self, x: int, y: int):
        while y <= 8:
            if (x, y) == self.current_empty_cell: return True
            y += 1
        return False
    
    def check_left(self, x: int, y: int):
        while x >= 0:
            if (x, y) == self.current_empty_cell: return True
            x -= 1
        return False

    def check_right(self, x: int, y: int):
        while x <= 8:
            if (x, y) == self.current_empty_cell: return True
            x += 1
        return False

    def handle_sliding(self, mouse_pos: tuple[int]):
        x, y = mouse_pos[0] // self.cell_size, mouse_pos[1] // self.cell_size

        if self.check_up(x, y):
            i = 0
            for pos, sprite in self.individual_sprite.items():
                if self.individual_sprite_positions[i][0] // self.cell_size == x and self.individual_sprite_positions[i][1] // self.cell_size <= y and self.individual_sprite_positions[i][1] // self.cell_size > self.current_empty_cell[1]:
                    self.individual_sprite_positions[i][1] -= self.cell_size
                i += 1
            self.current_empty_cell = x, y
        elif self.check_left(x, y):
            i = 0
            for pos, sprite in self.individual_sprite.items():
                if self.individual_sprite_positions[i][1] // self.cell_size == y and self.individual_sprite_positions[i][0] // self.cell_size <= x and self.individual_sprite_positions[i][0] // self.cell_size > self.current_empty_cell[0]:
                    self.individual_sprite_positions[i][0] -= self.cell_size
                i += 1
            self.current_empty_cell = x, y
        elif self.check_down(x, y):
            i = 0
            for pos, sprite in self.individual_sprite.items():
                if self.individual_sprite_positions[i][0] // self.cell_size == x and self.individual_sprite_positions[i][1] // self.cell_size >= y and self.individual_sprite_positions[i][1] // self.cell_size < self.current_empty_cell[1]:
                    self.individual_sprite_positions[i][1] += self.cell_size
                i += 1
            self.current_empty_cell = x, y
        elif self.check_right(x, y):
            i = 0
            for pos, sprite in self.individual_sprite.items():
                if self.individual_sprite_positions[i][1] // self.cell_size == y and self.individual_sprite_positions[i][0] // self.cell_size >= x and self.individual_sprite_positions[i][0] // self.cell_size < self.current_empty_cell[0]:
                    self.individual_sprite_positions[i][0] += self.cell_size
                i += 1
            self.current_empty_cell = x, y

    def randomize(self, level: int = 1000):
        for _ in range(level): self.handle_sliding((random.randint(0, self.image_size[0]), random.randint(0, self.image_size[1])))

    def is_solved(self):
        i = 0
        for pos, _ in self.individual_sprite.items():
            if pos != tuple(self.individual_sprite_positions[i]): return False
            i += 1
        return True

def main():

    puzzle = Puzzle("images/charizard.png", cell_size=400)
    puzzle.randomize()
    while True:
        events = pg.event.get()
        mouse = pg.mouse.get_pos()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                puzzle.handle_sliding(mouse)
                print(puzzle.is_solved())

        scr.fill((0, 0, 0))
        puzzle.render(scr)
        pg.display.flip()

if __name__ == "__main__": main()