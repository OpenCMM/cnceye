import bpy
import os


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
    output_folder = "/path/to/output_images"
    os.makedirs(output_folder, exist_ok=True)

    # Render images with different camera and light positions
    for i in range(10):
        camera_position = (
            camera_position_start[0] + i * 0.1,
            camera_position_start[1],
            camera_position_start[2],
        )
        output_path = os.path.join(output_folder, f"image_{i + 1}.png")
        render_image(output_path, camera_position, camera_rotation, light_position)

    print("Rendering completed!")
