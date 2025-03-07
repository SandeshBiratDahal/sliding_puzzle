import pygame as pg, sys, random, os

pg.init()

scr = pg.display.set_mode((800, 800))
clock = pg.time.Clock()
font = pg.font.Font(None, 32)

class Puzzle:
    def __init__(self, sprite_path: str, image_size: tuple[int] = (800, 800), cell_size: int = 100):
        self.full_sprite = pg.image.load(sprite_path).convert_alpha()
        self.cell_size = cell_size
        self.image_size = image_size
        self.full_sprite = pg.transform.scale(self.full_sprite, self.image_size)
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

def main(puzzle: Puzzle):
    puzzle.randomize(1000)
    while True:
        events = pg.event.get()
        mouse = pg.mouse.get_pos()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                puzzle.handle_sliding(mouse)
                if puzzle.is_solved(): return puzzle, winscreen

        scr.fill((0, 0, 0))
        puzzle.render(scr)
        clock.tick(60)
        pg.display.flip()

def winscreen(puzzle: Puzzle):
    opacity = 0
    while True:
        opacity += 3
        opacity = min(255, opacity)

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE: return None, mainmenu

        scr.fill((0, 0, 0))
        puzzle.render(scr)
        puzzle.full_sprite.set_alpha(opacity)
        scr.blit(puzzle.full_sprite, (0, 0))

        if opacity == 255:
            pg.draw.rect(scr, (255, 255, 255), [0, 800 - 32, 800, 132])
            scr.blit(
                font.render("You Won! Press <SPACE> to go to main menu!", True, (0, 0, 0)), (150, 800 - 24)
            )
        clock.tick(60)
        pg.display.flip()

def mainmenu(_):

    buttons = ["Start!", "Choose Image"]
    current_button = 0
    current_image = ""
    
    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w: current_button -= 1
                elif event.key == pg.K_s: current_button += 1

                current_button = max(current_button, 0)
                current_button = min(current_button, len(buttons) - 1)

                if event.key == pg.K_RETURN:
                    if current_button == 1:
                        current_image = image_selector()
                    
                    if current_button == 0:
                        if not current_image:
                            with open("settings.py", "r") as myfile:
                                current_image = eval(myfile.read())["current_image"]
                        puzzle = Puzzle(f"images/{current_image}", cell_size=200)
                        return puzzle, main

        scr.fill((135, 180, 255))
        for i, button in enumerate(buttons):
            color = "black"
            if i == current_button: color = "blue"
            text_render = font.render(button, True, color)
            scr.blit(text_render, (400 - text_render.get_width() // 2, 100 * i + 300))
            pg.draw.rect(scr, color, [400 - text_render.get_width() // 2 - 20, 100 * i + 300 - 20, text_render.get_width() + 40, text_render.get_height() + 40], 3)
        text_render = font.render("Use <W> and <S> to navigate and <ENTER> to select.", True, "black")
        scr.blit(text_render, (400 - text_render.get_width() // 2, 700))
        clock.tick(60)

        pg.display.flip()

def image_selector():
    files = os.listdir("images/")
    files = [file for file in files if file.endswith(".png") or file.endswith(".jpg")]

    current_button = 0
    buttons = files.copy()

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w: current_button -= 1
                elif event.key == pg.K_s: current_button += 1

                current_button = max(current_button, 0)
                current_button = min(current_button, len(buttons) - 1)

                if event.key == pg.K_RETURN:
                    with open("settings.py", "w") as myfile:
                        myfile.write(str({"current_image": buttons[current_button]}))
                    return buttons[current_button]

        scr.fill((135, 180, 255))
        for i, button in enumerate(buttons):
            color = "black"
            if i == current_button: color = "blue"
            text_render = font.render(button, True, color)
            scr.blit(text_render, (400 - text_render.get_width() // 2, 100 * i + 32 + 8))
            pg.draw.rect(scr, color, [400 - text_render.get_width() // 2 - 20, 100 * i + 20, text_render.get_width() + 40, text_render.get_height() + 40], 3)
        clock.tick(60)
        pg.display.flip()


if __name__ == "__main__": 
    args, section = None, mainmenu
    while True: args, section = section(args)