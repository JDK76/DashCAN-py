import os
import can
import datetime
import curses
import locale

locale.setlocale(locale.LC_ALL,"")
code = locale.getpreferredencoding()

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(0)
stdscr.clear()

#os.system('sudo ip link set can0 type can bitrate 1000000')
#os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')# socketcan_native

def show_bar(current_value, min_value, max_value, x, y, length):
	stdscr.addstr(y, x, "[")
	stdscr.addstr(y, x + length, "]")
	for i in range(0, length - 1):
		length_pc = float(i) / (length - 1)
		val_pc = float(current_value) / (max_value - min_value)
		if (length_pc < val_pc):
			stdscr.addstr(y, x + i + 1, u"\u2592".encode("utf-8"))
	#stdscr.addstr(y, x + length + 5, "length_pc: " + str(length_pc) + " val_pc: " + str(val_pc))

def bytes_to_int(bytes, start, end):
    result = 0
    i = start
    while i <= end:
        result = result * 256 + int(bytes[i])
        i += 1
    return result

def show_values():
	stdscr.clear()

	voffset = 0
	hoffset = 0
	stdscr.addstr(voffset + 0,hoffset + 0,"ENGINE",curses.A_BOLD | curses.A_UNDERLINE)
	stdscr.addstr(voffset + 1,hoffset + 0,"Speed",curses.A_BOLD)
	stdscr.addstr(voffset + 1,hoffset + 15,str(rpm) + " RPM")
	stdscr.addstr(voffset + 2,hoffset + 0,"Temp",curses.A_BOLD)
	stdscr.addstr(voffset + 2,hoffset + 15,str(coolant_temp) + " C")

	voffset = 0
	hoffset = 30
	stdscr.addstr(voffset + 0,hoffset + 0,"INLET",curses.A_BOLD | curses.A_UNDERLINE)
	stdscr.addstr(voffset + 1,hoffset + 0,"TPS",curses.A_BOLD)
	stdscr.addstr(voffset + 1,hoffset + 15,str(tps) + " %")
	stdscr.addstr(voffset + 2,hoffset + 0,"MAP",curses.A_BOLD)
	stdscr.addstr(voffset + 2,hoffset + 15,str(map) + " kPa")
	stdscr.addstr(voffset + 3,hoffset + 0,"Temp",curses.A_BOLD)
	stdscr.addstr(voffset + 3,hoffset + 15,str(air_temp) + " C")

	voffset = 5
	hoffset = 0
	stdscr.addstr(voffset + 0,hoffset + 0,"OIL",curses.A_BOLD | curses.A_UNDERLINE)
	stdscr.addstr(voffset + 1,hoffset + 0,"Pressure",curses.A_BOLD)
	stdscr.addstr(voffset + 1,hoffset + 15,str(oil_press) + " kPa")
	stdscr.addstr(voffset + 2,hoffset + 0,"Temp",curses.A_BOLD)
	stdscr.addstr(voffset + 2,hoffset + 15,str(oil_temp) + " C")

	voffset = 5
	hoffset = 30
	stdscr.addstr(voffset + 0,hoffset + 0,"FUEL",curses.A_BOLD | curses.A_UNDERLINE)
	stdscr.addstr(voffset + 1,hoffset + 0,"Pressure",curses.A_BOLD)
	stdscr.addstr(voffset + 1,hoffset + 15,str(fuel_press) + " kPa")
	stdscr.addstr(voffset + 2,hoffset + 0,"Temp",curses.A_BOLD)
	stdscr.addstr(voffset + 2,hoffset + 15,str(fuel_temp) + " C")
	stdscr.addstr(voffset + 3,hoffset + 0,"Composition",curses.A_BOLD)
	stdscr.addstr(voffset + 3,hoffset + 15,str(fuel_comp) + " % ethanol")
	stdscr.addstr(voffset + 4,hoffset + 0,"Level",curses.A_BOLD)
	stdscr.addstr(voffset + 4,hoffset + 15,str(fuel_level) + " L")

	voffset = 11
	hoffset = 0
	stdscr.addstr(voffset + 0,hoffset + 0,"OTHER",curses.A_BOLD | curses.A_UNDERLINE)
	stdscr.addstr(voffset + 1,hoffset + 0,"Accel pedal",curses.A_BOLD)
	stdscr.addstr(voffset + 1,hoffset + 15,str(accel_pedal) + " %")
	stdscr.addstr(voffset + 2,hoffset + 0,"Battery",curses.A_BOLD)
	stdscr.addstr(voffset + 2,hoffset + 15,str(voltage) + " v")
	stdscr.addstr(voffset + 3,hoffset + 0,"Vehicle speed",curses.A_BOLD)
	stdscr.addstr(voffset + 3,hoffset + 15,str(vss) + " km/h")
	stdscr.addstr(voffset + 4,hoffset + 0,"Gear",curses.A_BOLD)
	stdscr.addstr(voffset + 4,hoffset + 15,str(gear))

	stdscr.addstr(18,0,"Accel:",curses.A_BOLD)
	show_bar(accel_pedal, 0, 100, 7, 18, 70)
	stdscr.refresh()


def msg_dump():
	stdscr.clear()

	voffset = 0
	hoffset = 0
	sorted_ids = sorted(msgDict.keys())
	for msg_id in sorted_ids:
		if True: # msg_id >= 0x360: # and msg_id <= 0x374:
			hexstr = "".join("{:02x}".format(x) for x in msgDict[msg_id].data)
			stdscr.addstr(voffset,hoffset + 0,hex(msg_id) + " :",curses.A_BOLD)
			stdscr.addstr(voffset,hoffset + 8,hexstr)
			voffset += 1
			if voffset > 22:
				voffset = 0
				hoffset += 30


# 360
rpm = 0
map = 0.0
tps = 0.0
# 361
fuel_press = 0.0
oil_press = 0.0
# 370
vss = 0.0
gear = 0
# 372
voltage = 0.0
# 3E0
coolant_temp = 0.0
air_temp = 0.0
fuel_temp = 0.0
oil_temp = 0.0
# 3E1
fuel_comp = 0.0
# 3E2
fuel_level = 0.0
#471
accel_pedal = 0.0

msgDict = {}

dt = datetime.datetime.now()

continue_flag = True
while continue_flag:
	msg = can0.recv(0.5)

	if msg is None:
		#print('Timeout occurred, no message.')
		#continue_flag = False
		continue

	if msg is not None and msg.arbitration_id is not None:
		if msg.arbitration_id is None:
			continue
		msgDict[msg.arbitration_id] = msg

	if msg.arbitration_id == 864 and len(msg.data) == 8:
		rpm = bytes_to_int(msg.data,0,1)
		map = bytes_to_int(msg.data,2,3) / 10.0
		tps = bytes_to_int(msg.data,4,5) / 10.0

	if msg.arbitration_id == 865 and len(msg.data) == 8:
		fuel_press = bytes_to_int(msg.data,0,1) / 10.0 - 101.3
		oil_press = bytes_to_int(msg.data,2,3) / 10.0 - 101.3

	if msg.arbitration_id == 880 and len(msg.data) == 8:
		vss = bytes_to_int(msg.data,0,1) / 10.0
		gear = bytes_to_int(msg.data,0,1)

	if msg.arbitration_id == 882 and len(msg.data) == 8:
		voltage = bytes_to_int(msg.data,0,1) / 10.0

	if msg.arbitration_id == 992 and len(msg.data) == 8:
		coolant_temp = bytes_to_int(msg.data,0,1) / 10.0 - 273.15
		air_temp = bytes_to_int(msg.data,2,3) / 10.0 - 273.15
		fuel_temp = bytes_to_int(msg.data,4,5) / 10.0 - 273.15
		oil_temp = bytes_to_int(msg.data,6,7) / 10.0 - 273.15

	if msg.arbitration_id == 993 and len(msg.data) == 8:
		fuel_comp = bytes_to_int(msg.data,4,5) / 10.0

	if msg.arbitration_id == 994 and len(msg.data) == 8:
		fuel_level = bytes_to_int(msg.data,0,1) / 10.0

	if msg.arbitration_id == 0x471 and len(msg.data) == 8:
		accel_pedal = bytes_to_int(msg.data,2,3) / 10.0

	ms_count = (datetime.datetime.now() - dt).total_seconds() * 1000.0
	if ms_count > 100:
		dt = datetime.datetime.now()

		show_values()
		#msg_dump()

	stdscr.nodelay(True)
	if stdscr.getch() != curses.ERR:
		continue_flag = False

#os.system('sudo ifconfig can0 down')

curses.curs_set(1)
stdscr.keypad(False)
curses.nocbreak()
curses.echo()
curses.endwin()
