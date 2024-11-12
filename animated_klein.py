import math

import bpy
from mathutils import Vector

# Step 1: Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Step 2: Create an approximate Klein bottle (using a torus with modifications)
bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.3, major_segments=48, minor_segments=12)
klein_bottle = bpy.context.object
klein_bottle.name = "Klein_Bottle"

# Step 3: Apply textures and materials

# Handle material
handle_material = bpy.data.materials.new(name="HandleMaterial")
handle_material.use_nodes = True
nodes = handle_material.node_tree.nodes
nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1)  # Red color
klein_bottle.data.materials.append(handle_material)

# Apply other textures, including Chinese writings texture
texture_material = bpy.data.materials.new(name="TextureMaterial")
texture_material.use_nodes = True
tex_image = nodes.new(type="ShaderNodeTexImage")
tex_image.image = bpy.data.images.load("/home/talles/Downloads/Enviroments/Psychoanalysis/textures/Poliigon_BrickWallReclaimed_8320/Poliigon_BrickWallReclaimed_8320_Preview1.png")  # Replace with actual path
nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.8, 0.8, 1)  # Grayish base
nodes.link(tex_image.outputs["Color"], nodes["Principled BSDF"].inputs["Base Color"])
klein_bottle.data.materials.append(texture_material)

# Upholstery: Use another texture material for covering
upholstery_material = bpy.data.materials.new(name="UpholsteryMaterial")
upholstery_material.use_nodes = True
upholstery_texture = nodes.new(type="ShaderNodeTexImage")
upholstery_texture.image = bpy.data.images.load("/home/talles/Downloads/Enviroments/Psychoanalysis/textures/Poliigon_RattanWeave_6945/Poliigon_RattanWeave_6945_Preview1.png")  # Replace with actual path
nodes["Principled BSDF"].inputs[0].default_value = (0.6, 0.3, 0.2, 1)  # Brownish tone
nodes.link(upholstery_texture.outputs["Color"], nodes["Principled BSDF"].inputs["Base Color"])
klein_bottle.data.materials.append(upholstery_material)

# Step 4: Create animations

# Animation: Increase/decrease proportions
klein_bottle.scale = (1, 1, 1)
klein_bottle.keyframe_insert(data_path="scale", frame=1)
klein_bottle.scale = (1.2, 0.8, 1)  # Change proportions
klein_bottle.keyframe_insert(data_path="scale", frame=30)

# Animation: Wave effect
modifier = klein_bottle.modifiers.new(name="Wave", type='WAVE')
modifier.speed = 0.2
modifier.width = 0.5
modifier.height = 0.1
modifier.start_position_x = 0
bpy.context.scene.frame_end = 100  # Set the end of the animation

# Step 5: Add shadow/coverage with lighting

# Add light source
bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
light = bpy.context.object
light.data.energy = 300

# Step 6: Interaction with multiple bottles

# Duplicate Klein bottle for interaction
bottle1 = klein_bottle
bottle2 = klein_bottle.copy()
bottle2.location = (3, 0, 0)
bpy.context.collection.objects.link(bottle2)

# Set up interaction animation
bottle1.location = (0, 0, 0)
bottle1.keyframe_insert(data_path="location", frame=1)
bottle1.location = (1, 1, 0)
bottle1.keyframe_insert(data_path="location", frame=50)

bottle2.location = (3, 0, 0)
bottle2.keyframe_insert(data_path="location", frame=1)
bottle2.location = (2, 1, 0)
bottle2.keyframe_insert(data_path="location", frame=50)

# Step 7: Different costumes with holes
for material in [texture_material, upholstery_material]:
    material.use_nodes = True
    node_tree = material.node_tree
    bsdf = node_tree.nodes["Principled BSDF"]
    texture = node_tree.nodes.get("Image Texture")
    if texture:
        texture.extension = 'CLIP'  # To clip holes

# Set up camera
bpy.ops.object.camera_add(location=(5, -5, 3))
camera = bpy.context.object
bpy.context.scene.camera = camera
camera.rotation_euler = (math.radians(60), 0, math.radians(45))

# Finalize and render animation settings
bpy.context.scene.render.filepath = "/home/talles/Downloads/Enviroments/Psychoanalysis/animations/"
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'MPEG4'
bpy.context.scene.render.ffmpeg.codec = 'H264'

print("Setup complete. Run animation in Blender to see results.")

