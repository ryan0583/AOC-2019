import tkinter as tk
from Utils.point import Point


class GraphicsPanel:
    def __init__(self, tiles):
        self.tiles = tiles
        self.rects = {}
        self.root = tk.Tk()
        self.canvas = None
        self.text_component = None

    @staticmethod
    def create_empty_panel(x_dim, y_dim):
        tile_map = {}
        for x in range(0, x_dim):
            for y in range(0, y_dim):
                tile_map[Point(x, y)] = "black"
        return GraphicsPanel(tile_map)

    def reset(self):
        for point in self.tiles.keys():
            self.update_canvas(point, "black")

    def update_canvas_with_offset(self, point, color, x_offset, y_offset):
        normalised_point = Point(x_offset + point.x, y_offset + point.y)
        self.update_canvas(normalised_point, color)

    def update_canvas(self, point, color):
        rect = self.rects.get(point)
        if rect is None:
            rect = self.canvas.create_rectangle(point.x * GAME_SCALE, point.y * GAME_SCALE,
                                                point.x * GAME_SCALE + GAME_SCALE,
                                                point.y * GAME_SCALE + GAME_SCALE, fill=color)
            self.rects[point] = rect
        else:
            self.canvas.itemconfigure(rect, fill=color)

    def paint_canvas(self):
        self.root.update_idletasks()
        self.root.update()

    def init_canvas(self):
        x_dimension = (max(list(map(lambda position: position.x, self.tiles.keys()))) + 1) * GAME_SCALE
        y_dimension = (max(list(map(lambda position: position.y, self.tiles.keys()))) + 1) * GAME_SCALE

        self.canvas = tk.Canvas(self.root, width=x_dimension, height=y_dimension)
        self.canvas.pack()

        for point in self.tiles.keys():
            color = self.tiles.get(point)
            self.update_canvas(point, color)

    def add_text(self, text, color):
        self.text_component = self.canvas.create_text(GAME_SCALE * 2, GAME_SCALE * 2, fill=color,
                                font="Arial " + str(GAME_SCALE - GAME_SCALE // 2), anchor="w",
                                text=text)

    def update_text(self, text):
        self.canvas.itemconfigure(self.text_component, text=text)


GAME_SCALE = 10
