import csv

def load_gcode(filepath: str):
    with open(filepath, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        gcode = list(reader)
    gcode = gcode[2:-2]
    return gcode

def test_load_gcode():
	filepath = "tests/fixtures/gcode/edge.gcode"
	gcode = load_gcode(filepath)
	breakpoint()
	assert len(gcode) == 16