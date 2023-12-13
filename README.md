# cnceye
![Test](https://github.com/OpenCMM/cnceye/actions/workflows/ci.yml/badge.svg)

cnceye analyzes 3D models from a stl file and find measuring lines and curves.

![a laser triagulation sensor](https://opencmm.xyz/assets/images/sensor-55b7cf98350f293eba2c2b9d593bdd4f.png)

## Installation
```bash
pip install cnceye
```

## Usage

```python
from cnceye import Shape

shape = Shape("tests/fixtures/stl/sample.stl")
lines, arcs = shape.get_lines_and_arcs()
```

## Simulation with Blender
Create test data

Prerequisites 
- Blender 3.6.1 or later

```bash
blender "blender/measure.blend" --background --python scripts/demo.py -- tests/fixtures/gcode/edge.gcode
```