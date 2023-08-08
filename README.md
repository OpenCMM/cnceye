# cnceye
![Test](https://github.com/OpenCMM/cnceye/actions/workflows/ci.yml/badge.svg)

An image-based CMM (Coordinate Measuring Machine) system for CNC machine tools

## Simulation with Blender
Create test data

Prerequisites 
- Blender 3.6.1 or later

Change the output path in `scripts/create_test_images.py` and run

```bash
blender "blender/example.blend" --background --python scripts/create_test_images.py
```