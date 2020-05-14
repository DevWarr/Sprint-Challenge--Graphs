from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


def make_path_tuple(d):
    if d == "n":
        return ("n", None, "s")
    if d == "s":
        return ("s", None, "n")
    if d == "e":
        return ("e", None, "w")
    if d == "w":
        return ("w", None, "e")


traversal_path = []
graph = {}
dead_ends = {}
graph[player.current_room.id] = {
    d: None for d in player.current_room.get_exits()}
# Tuple: (direction_in, room_id, direction_out)
path = [(None, player.current_room.id, None)]


def move_backwards_if_needed():
    while True:
        if any(graph[path[-1][1]][d] is None for d in graph[path[-1][1]]):
            return
        r = path.pop()
        traversal_path.append(r[2])
        player.travel(r[2])


def create_graph_and_traverse():
    while True:

        if path[-1][0] is not None:
            # If we can move, move!
            traversal_path.append(path[-1][0])
            player.travel(path[-1][0])

            # Update the path info in our path stack and the graph
            path[-1] = (path[-1][0], player.current_room.id, path[-1][2])
            graph[path[-2][1]][path[-1][0]] = player.current_room.id
            if path[-1][1] not in graph:
                graph[path[-1][1]
                      ] = {d: None for d in player.current_room.get_exits()}
                graph[path[-1][1]][path[-1][2]] = path[-2][1]

        # We check if our graph is complete just after we move,
        # but just before we set up our next move
        if len(graph) == len(room_graph):
            break

        if len(graph[path[-1][1]]) == 1:
            dead_ends[path[-1][1]] = True
        move_backwards_if_needed()

        for d in graph[path[-1][1]]:
            if graph[path[-1][1]][d] is None:
                path.append(make_path_tuple(d))
                break
    # print(dead_ends)


def bfs(start, end):
    # q = queue, r = room, t = travel direction
    visited = {start: True}
    q = [(start, [])]

    while len(q) > 0:
        r = q.pop(0)
        for t in graph[r[0]]:

            if graph[r[0]][t] == end:
                return [*r[1], t]

            elif graph[r[0]][t] not in visited:
                visited[graph[r[0]][t]] = True
                q.append((graph[r[0]][t], [*r[1], t]))


def try_bfs_traversal():
    full_path = []
    start = world.starting_room.id
    while len(dead_ends) > 0:
        closest_lookup = {}
        for room in dead_ends:
            closest_lookup[room] = bfs(start, room)

        closest_room = list(closest_lookup.keys())[0]
        for path in closest_lookup:
            if len(closest_lookup[path]) < len(closest_lookup[closest_room]):
                closest_room = path

        full_path += closest_lookup[closest_room]
        dead_ends.pop(closest_room)
        start = closest_room
        # print(closest_lookup[closest_room])
    return full_path


create_graph_and_traverse()
# traversal_path = try_bfs_traversal()
# print(len(traversal_path))

def main():
    # TRAVERSAL TEST
    visited_rooms = set()
    player.current_room = world.starting_room
    player.current_room.visited = True
    visited_rooms.add(player.current_room)

    for move in traversal_path:
        player.travel(move)
        visited_rooms.add(player.current_room)

    # world.print_rooms()

    if len(visited_rooms) == len(room_graph):
        print(
            f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
    else:
        print("TESTS FAILED: INCOMPLETE TRAVERSAL")
        print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


def repl():
    player.current_room.print_room_description(player)
    while True:
        cmds = input("-> ").lower().split(" ")
        if cmds[0] in ["n", "s", "e", "w"]:
            player.travel(cmds[0], True)
        elif cmds[0] == "q":
            break
        else:
            print("I did not understand that command.")


if __name__ == "__main__":
    main()
    # repl()
    exit()
