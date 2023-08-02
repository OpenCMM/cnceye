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
    # Define camera and light positions
    camera_position_start = (-0.05, 0.025, 0.06)
    camera_rotation = (0.0, 0.0, 0.0)
    light_position = (0, 0, 0.1)

    # Create a folder to save the rendered images
    output_folder = "/home/runner/work/cnceye/cnceye/output"
    os.makedirs(output_folder, exist_ok=True)

    # Render images with different camera and light positions
    index = 0
    for i in range(6):
        for j in range(6):
            camera_position = (
                camera_position_start[0] + j * 0.02,
                camera_position_start[1] - i * 0.01,
                camera_position_start[2],
            )
            output_path = os.path.join(output_folder, f"image_{index}.png")
            render_image(output_path, camera_position, camera_rotation, light_position)
            index += 1
            sleep(0.1)

    print("Rendering completed!")
