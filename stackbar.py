import dearpygui.dearpygui as dpg

class stackbar:
    def __init__(self, name:str, stacked:bool, flash_on_max:bool, min_label:str, max_label:str, min_value:float, max_value:float) -> None:
        self.viewport_name = "viewport_" + name
        self.stacked = stacked
        self.flash_on_max = flash_on_max
        self.min_label = min_label
        self.max_label = max_label
        self.min_value = min_value
        self.max_value = max_value
        self.full_range = max_value - min_value
        self.segment_range = self.full_range / 10.0

        dpg.add_viewport_drawlist(front=False, tag=self.viewport_name)
        self.fontregistry_name = "fontregistry_" + name
        with dpg.font_registry(tag=self.fontregistry_name):
            self.default_font = dpg.add_font("square721_bt_bold.ttf", 130, parent=self.fontregistry_name)

    def draw_rect(self, left, top, width, height, *, margin=(0,0), color=[], fill=[], thickness=0):
        return dpg.draw_rectangle((left + margin[0], top + margin[1]), (left + width - margin[0], top + height - margin[1]), color=color, fill=fill, thickness=thickness, parent=self.viewport_name)

    def draw_poly(self, points, *, origin=[], color=[], fill=[], thickness=0):
        adjusted_points = []
        if (len(origin) == 2):
            for x in points:
                adjusted_points.append((x[0] + origin[0], x[1] + origin[1]))
        dpg.draw_polygon(adjusted_points, color=color, fill=fill, thickness=thickness, parent=self.viewport_name)

    def draw_text(self, pos, text, *, size:float=10, color=None, font:(int | str)=None):
        t = dpg.draw_text(pos=pos, text=text, size=size, color=color, parent=self.viewport_name)
        if ((font is not None)):
            dpg.bind_item_font(t, font)

    def draw_segment(self, origin: tuple[int,int], idx:int, lit:bool):
        left = origin[0] + 120
        top = origin[1] + 50 + (idx) * 100
        color = self.segment_unlit
        if (lit):
            color = self.segment_lit
        self.draw_rect(left, top, 260, 100, margin=(7.5, 5), fill=color, color=color)

    def draw_segments(self, origin: tuple[int,int], val:int):
        for seg_no in range(1, 11):
            is_lit = False
            if (val >= (self.min_value + (self.segment_range * (seg_no - 1)))):
                if (self.stacked):
                    is_lit = True
                else:
                    if (val < (self.segment_range * seg_no)):
                        is_lit = True
            self.draw_segment(origin, 10 - seg_no, is_lit)

    def draw(self, origin: tuple[int,int]):
        # outline
        self.draw_rect(origin[0], origin[1], 500, 1100, color=(255,255,255), thickness=1)

        # segment elements
        self.draw_segments(origin, 0)

        # border
        self.draw_rect(origin[0] + 120, origin[1] + 50, 260, 1000, color=self.segment_lit, thickness=5)

        # pointer
        self.draw_poly(((0,0), (40, 25), (0, 50)), origin=(origin[0] + 50, origin[1] + 525), color=self.segment_lit, fill=self.segment_lit)

        # labels
        self.draw_text((origin[0] + 25, origin[1] + 22), text=self.max_label, size=130, color=self.segment_lit, font=self.default_font)
        self.draw_text((origin[0] + 25, origin[1] + 947), text=self.min_label, size=130, color=self.segment_lit, font=self.default_font)

        dpg.create_context()

    def set_value(self, origin: tuple[int,int], val: int):
        self.draw_segments(origin, val)

    segment_lit = (56, 193, 150)
    segment_unlit = (20, 29, 30)
    segment_background = (16, 25, 26)