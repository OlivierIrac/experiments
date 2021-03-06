'''
Created on 29 juin 2017

@author: irac1
'''


def resizeProportional(x1, y1, x2, y2):
    xRatio = float(x2) / float(x1)
    yRatio = float(y2) / float(y1)
    if (xRatio > yRatio):
        x1 = yRatio * x1
        y1 = y2
    else:
        x1 = x2
        y1 = xRatio * y1
    return (int(x1), int(y1))


def blit_text(surface, text, pos, font, color=(0, 0, 0)):
    # 2D array where each row is a list of words.
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # The width of a space.
    max_width = surface.get_width()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
