import pygame
import random
import math

pygame.init()


class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    PINK = 251, 72, 196
    BACKGROUND_COLOR = 12, 12, 12

    GRAY = [(128, 128, 128),
            (160, 160, 160),
            (192, 192, 192)]

    FONT = pygame.font.SysFont('comicsans', 15)
    LARGE_FONT = pygame.font.SysFont('comicsans', 20)
    SIDE_PAD = 100  # px
    TOP_PAD = 150  # px

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = math.floor((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2  # start at half of padding


def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    controls = draw_info.FONT.render("R - Reset |"
                                     " SPACE - Start Sorting |"
                                     " A - Ascending |"
                                     " D - Descending", 1, draw_info.WHITE)  # antialias
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 5))

    sortText = draw_info.FONT.render("B - Bubble Sort |"
                                     " I - Insertion Sort", 1, draw_info.WHITE)  # antialias
    draw_info.window.blit(sortText, (draw_info.width / 2 - sortText.get_width() / 2, 35))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)

        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRAY[i % 3] # cycle through the 3 grays

        if i in color_positions:
            color = color_positions[i]

        # draw the bar
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


# algorythms
def bubble_sort(draw_info, ascending=True):  # true default
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]  # swap values in one line without temp values
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.PINK}, True)
                yield True  # pauses the function until it is called again (yield control)
    return lst


# render screen
def main():
    clock = pygame.time.Clock()  # regulates loop time

    n = 100
    min_val = 0
    max_val = 300

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInfo(800, 600, lst)
    sorting = False
    ascending = True

    sorting_alg = bubble_sort
    sorting_alg_name = "Bubble Sort"
    sorting_alg_generator = None

    run = True
    while run:
        clock.tick(4800)

        if sorting:
            try:
                next(sorting_alg_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info)

        # render display
        pygame.display.update()

        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:  # reset the list on R
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
            elif event.key == pygame.K_SPACE and sorting == False:  # start sorting on SPACE if not already
                sorting = True
                sorting_alg_generator = sorting_alg(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:  # ascending
                ascending = True
            elif event.key == pygame.K_d and not sorting:  # descending
                ascending = False

    pygame.quit()


if __name__ == "__main__":
    main()


