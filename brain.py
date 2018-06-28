"""
Brian Silverman's Brain
"""


import numpy as np
import pygame as pg
import pygame.locals as lcls

from pygame import surfarray as sf

SIZE = 500
ZOOM = 1000 // SIZE
P_ACTIVE = 1 / 250

FRAMERATE = 30
DELAY_MS = 1000 // FRAMERATE


def _sum(src):
    dst = np.zeros_like(src)
    dst[1:, :] += src[:-1, :]
    dst[:-1, :] += src[1:, :]
    dst[:, 1:] += src[:, :-1]
    dst[:, :-1] += src[:, 1:]
    dst[1:, 1:] += src[:-1, :-1]
    dst[1:, :-1] += src[:-1, 1:]
    dst[:-1, 1:] += src[1:, :-1]
    dst[:-1, :-1] += src[1:, 1:]
    return dst


def _update(off, active, cooldown, colors):
    """
    active -> cooldown
    cooldown -> off
    off -> active if exactly two neighbours are active
    """

    total = _sum(active)
    total[off == 0] = 0
    # Now total contains number of active neighbours, but is zeroed
    # for non-empty cells

    # print("======")
    # print("off\n", off)
    # print("active\n", active)
    # print("cooldown\n", cooldown)
    # print("total\n", total)

    # cooldown -> off
    off += cooldown

    # active -> cooldown
    cooldown[:] = active[:]

    # off -> active if...

    # We start with empty active plane
    active[:] = 0
    active[total == 2] = 1
    off[total == 2] = 0

    colors[:] = (0., 67., 88.)
    colors[active > 0] = (253., 116., 0.)
    colors[cooldown > 0] = (190., 219., 57.)


def main(size, zoom, init_p):
    """Entry point."""
    # pylint:disable=no-member
    pg.init()

    random = np.random.rand(size, size)
    off = np.zeros((size, size), dtype=int)
    active = np.zeros((size, size), dtype=int)
    cooldown = np.zeros((size, size), dtype=int)
    active[random < init_p] = 1

    off[active == 0] = 1

    colors = np.zeros((size, size, 3), dtype=float)

    screen = pg.display.set_mode((size * zoom, size * zoom), 0, 24)
    # pylint:disable=too-many-function-args
    surface = pg.Surface((size, size))
    while True:
        loop_start_ms = pg.time.get_ticks()
        evt = pg.event.poll()
        if evt.type == lcls.QUIT:
            pg.image.save(screen, "out.png")
            raise SystemExit()
        _update(off, active, cooldown, colors)

        sf.blit_array(surface, colors)
        pg.transform.scale(surface, (size * zoom, size * zoom), screen)
        loop_end_ms = pg.time.get_ticks()
        if loop_end_ms > loop_start_ms + DELAY_MS:
            print("WARNING: too slow for desired framerate")
        else:
            pg.time.delay(loop_start_ms + DELAY_MS - loop_end_ms)
        pg.display.flip()


if __name__ == '__main__':
    main(SIZE, ZOOM, P_ACTIVE)
