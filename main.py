import copy
import tcod

import color
import entity_factories
from engine import Engine
from procgen import generate_dungeon


def main():
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player)

    engine.game_map = generate_dungeon(
        max_rooms,
        room_min_size,
        room_max_size,
        map_width,
        map_height,
        max_monsters_per_room,
        engine,
    )

    engine.update_fov()

    engine.message_log.add_message(
        "Welcome to the dungeon, player!", color.welcome_text
    )

    # Creating the screen
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Demo Roguelike",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:

            engine.render(root_console, context)

            engine.event_handler.handle_events()


if __name__ == '__main__':
    main()
