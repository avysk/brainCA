"""
Brian Silverman's Brain
"""

import argparse
import logging

import imageio.v2 as iio
import numpy as np
import pygame as pg
import pygame.locals as lcls

from pygame import surfarray as sf

logger = logging.getLogger(__name__)

SIZE = 500
ZOOM = 2
P_ACTIVE = 1 / 250
FRAMERATE = 30
GENERATIONS = 0


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

    # cooldown -> off
    off += cooldown

    # active -> cooldown
    cooldown[:] = active[:]

    # off -> active if...

    # We start with empty active plane
    active[:] = 0
    active[total == 2] = 1
    off[total == 2] = 0

    colors[:] = (0.0, 67.0, 88.0)
    colors[active > 0] = (253.0, 116.0, 0.0)
    colors[cooldown > 0] = (190.0, 219.0, 57.0)


def main(size, zoom, init_p, framerate, generations, picture, video):
    """Entry point."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Parameters:")
    logger.info("  size: %d", size)
    logger.info("  zoom: %d", zoom)
    logger.info("  init_p: %s", init_p)
    logger.info("  framerate: %d", framerate)
    if generations == 0:
        logger.info("  generations: indefinite")
    else:
        logger.info("  generations: %d", generations)
    if picture:
        logger.info("  picture: %s", picture)
    else:
        logger.info("  picture: will not be saved")
    if video:
        logger.info("  video: %s", video)
    else:
        logger.info("  video: will not be saved")

    delay_ms = 1000 // framerate
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

    writer = None
    if video:
        writer = iio.get_writer(video, fps=framerate)

    gen = 0
    running = True
    while running:
        loop_start_ms = pg.time.get_ticks()
        evt = pg.event.poll()
        if evt.type == lcls.QUIT:
            running = False
        _update(off, active, cooldown, colors)
        gen += 1
        if generations > 0 and gen >= generations:
            running = False

        sf.blit_array(surface, colors)
        pg.transform.scale(surface, (size * zoom, size * zoom), screen)
        loop_end_ms = pg.time.get_ticks()
        if loop_end_ms > loop_start_ms + delay_ms:
            logger.warning("too slow for desired framerate")
        else:
            pg.time.delay(loop_start_ms + delay_ms - loop_end_ms)
        pg.display.flip()

        if writer:
            frame = pg.surfarray.array3d(screen)
            frame = np.transpose(frame, (1, 0, 2))
            writer.append_data(frame)

    if picture:
        pg.image.save(screen, picture)
    if writer:
        writer.close()
    raise SystemExit()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Brian's Brain - a 2D cellular automaton simulation"
    )
    parser.add_argument(
        "-s", "--size", type=int, default=SIZE, help=f"Grid size (default: {SIZE})"
    )
    parser.add_argument(
        "-z",
        "--zoom",
        type=int,
        default=ZOOM,
        help=f"Display zoom factor (default: {ZOOM})",
    )
    parser.add_argument(
        "-i",
        "--init-p-active",
        type=float,
        default=P_ACTIVE,
        dest="p_active",
        help=f"Initial probability of a cell being active (default: {P_ACTIVE})",
    )
    parser.add_argument(
        "-f",
        "--framerate",
        type=int,
        default=FRAMERATE,
        help=f"Target frames per second (default: {FRAMERATE})",
    )
    parser.add_argument(
        "-g",
        "--generations",
        type=int,
        default=GENERATIONS,
        help=f"Exit after N generations (default: {GENERATIONS}, run indefinitely)",
    )
    parser.add_argument(
        "-p",
        "--picture",
        type=str,
        default=None,
        dest="picture",
        help="Save final screenshot to FILE",
    )
    parser.add_argument(
        "-v",
        "--video",
        type=str,
        default=None,
        dest="video",
        help="Save video to FILE (e.g., output.mp4)",
    )
    return parser.parse_args()


def run():
    """Entry point for installed script."""
    args = parse_args()
    zoom = args.zoom
    main(
        args.size,
        zoom,
        args.p_active,
        args.framerate,
        args.generations,
        args.picture,
        args.video,
    )


if __name__ == "__main__":
    run()
