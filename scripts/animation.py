import bpy
from mathutils import Vector

# Set the current frame to frame 1 (start of the animation)
bpy.context.scene.frame_set(1)

# Get the object you want to animate
obj = bpy.data.objects["sensor"]

# Set the initial location (frame 1)
obj.location = Vector((0.0567, 0.0316, 0.206))
obj.keyframe_insert(data_path="location", frame=1)

current_frame = 1
length = 0.057
width = 0.11
y_move = 0.005

for i in range(1, 6):
    # move x axis
    current_frame = i * 30 + (i - 1) * 10
    bpy.context.scene.frame_set(current_frame)
    if i % 2 == 0:
        x = obj.location[0] + width
    else:
        x = obj.location[0] - width
    obj.location = (x, obj.location[1], obj.location[2])
    obj.keyframe_insert(data_path="location", frame=current_frame)

    # move y axis
    bpy.context.scene.frame_set(i * 40)
    y = obj.location[1] + y_move
    obj.location = (x, y, obj.location[2])
    obj.keyframe_insert(data_path="location", frame=i * 40)

# save changes
bpy.ops.wm.save_mainfile()

# run animation
# bpy.ops.screen.animation_play()
