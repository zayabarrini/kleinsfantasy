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

# Step 3: Apply materials and textures

# Handle material (Red Color)
handle_material = bpy.data.materials.new(name="HandleMaterial")
handle_material.use_nodes = True
klein_bottle.data.materials.append(handle_material)  # Attach material to object

# Texture Material (with Chinese writing texture)
texture_material = bpy.data.materials.new(name="TextureMaterial")
texture_material.use_nodes = True
klein_bottle.data.materials.append(texture_material)  # Attach material to object

# Access nodes in the new material
nodes = texture_material.node_tree.nodes
tex_image = nodes.new(type="ShaderNodeTexImage")
tex_image.image = bpy.data.images.load("/home/zaya/Downloads/Workspace/Animations/Textures/Poliigon_SlateFloorTile_7657/Poliigon_SlateFloorTile_7657_Preview1.png")  # Replace with actual path
bsdf = nodes.get("Principled BSDF")  # Principled BSDF node is created by default
if bsdf:  # Only proceed if BSDF node exists
    texture_material.node_tree.links.new(tex_image.outputs["Color"], bsdf.inputs["Base Color"])

# Upholstery Material
upholstery_material = bpy.data.materials.new(name="UpholsteryMaterial")
upholstery_material.use_nodes = True
klein_bottle.data.materials.append(upholstery_material)  # Attach material to object

# Add an upholstery texture
nodes = upholstery_material.node_tree.nodes
upholstery_texture = nodes.new(type="ShaderNodeTexImage")
upholstery_texture.image = bpy.data.images.load("/home/zaya/Downloads/Workspace/Animations/Textures/Poliigon_RattanWeave_6945/Poliigon_RattanWeave_6945_Preview1.png")  # Replace with actual path
bsdf = nodes.get("Principled BSDF")
if bsdf:
    upholstery_material.node_tree.links.new(upholstery_texture.outputs["Color"], bsdf.inputs["Base Color"])

# Step 4: Animate Proportions and Wave Effect
klein_bottle.scale = (1, 1, 1)
klein_bottle.keyframe_insert(data_path="scale", frame=1)
klein_bottle.scale = (1.2, 0.8, 1)
klein_bottle.keyframe_insert(data_path="scale", frame=30)

# Apply a wave modifier for a wavy effect
modifier = klein_bottle.modifiers.new(name="Wave", type='WAVE')
modifier.speed = 0.2
modifier.width = 0.5
modifier.height = 0.1

# Animation range settings
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 100


