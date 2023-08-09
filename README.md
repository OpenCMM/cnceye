# cnceye
![Test](https://github.com/OpenCMM/cnceye/actions/workflows/ci.yml/badge.svg)

Cnceye indentifies the actual coordiantes of each vertex of a product from a image.
From there, it will measure the dimensions of the product. Our goal is to make this process as easy as possible with less than 1 micro precision.


## Simulation with Blender
Create test data

Prerequisites 
- Blender 3.6.1 or later

Change the output path in `scripts/create_test_images.py` and run

```bash
blender "blender/example.blend" --background --python scripts/create_test_images.py
```