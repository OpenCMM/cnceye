import bpy
import os
from time import sleep


def render_image(output_path, camera_position, camera_rotation, light_position):
    # Set camera position and rotation
    camera = bpy.data.objects["Camera"]
    camera.location = camera_position
    camera.rotation_euler = camera_rotation

    # Set light position
    lamp = bpy.data.objects["Light"]
    lamp.location = light_position

    # Set rendering settings
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.filepath = output_path

    # Render the image
    bpy.ops.render.render(write_still=True)


# Example usage
if __name__ == "__main__":
    # set unit to millimeters
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.length_unit = "MILLIMETERS"

    # Define camera and light positions
    camera_rotation = (0.0, 0.0, 0.0)

    # Create a folder to save the rendered images
    output_folder = "/path/to/output_images"
    os.makedirs(output_folder, exist_ok=True)

    # Render images with different camera and light positions
    index = 0
    with open("coordinates.txt") as f:
        for line in f:
            xyz = line.strip().split(",")
            x, y, z = [float(i)/1000 for i in xyz]
            camera_position = (x, y, 0.0105)
            light_position = (x, y, 0.1)
            output_path = os.path.join(output_folder, f"image_{index}.png")
            render_image(output_path, camera_position, camera_rotation, light_position)
            index += 1
            sleep(0.1)

    print("Rendering completed!")
