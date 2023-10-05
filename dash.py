import dearpygui.dearpygui as dpg
import stackbar as sb

dpg.create_context()

fuel = sb.stackbar("fuel", True, False, "E", "F", 0, 100)
fuel.draw((30,30))
fuel.set_value((30,30), 11)

temp = sb.stackbar("temp", False, True, "C", "H", 0, 150)
temp.draw((600,30))
temp.set_value((600,30), 74)

dpg.create_viewport(title='DashCAN', width=1200, height=1200, x_pos=50, y_pos=50)
dpg.setup_dearpygui()
dpg.show_viewport(maximized=True)
dpg.start_dearpygui()
dpg.destroy_context()