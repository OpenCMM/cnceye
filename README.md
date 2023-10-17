# cnceye
![Test](https://github.com/OpenCMM/cnceye/actions/workflows/ci.yml/badge.svg)

cnceye measures the dimensions of a workpiece using the a laser triagulation sensor on a CNC machine.

![a laser triagulation sensor](https://opencmm.xyz/assets/images/sensor-55b7cf98350f293eba2c2b9d593bdd4f.png)

## Simulation with Blender
Create test data

Prerequisites 
- Blender 3.6.1 or later

```bash
blender "blender/measure.blend" --background --python scripts/demo.py -- tests/fixtures/gcode/edge.gcode
```