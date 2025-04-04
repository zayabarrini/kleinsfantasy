import math
import os
import bpy
from mathutils import Vector

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create Klein bottle
bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.3, 
                                major_segments=48, minor_segments=12)
klein_bottle = bpy.context.object
klein_bottle.name = "Klein_Bottle"

# ========== MATERIAL SETUP ==========
def create_material(name, color, texture_path=None):
    """Helper function to create materials with optional textures"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create essential nodes
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = color
    output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Add texture if provided
    if texture_path:
        tex = nodes.new(type='ShaderNodeTexImage')
        try:
            tex.image = bpy.data.images.load(texture_path)
            links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
        except:
            print(f"Texture not found: {texture_path}")
    
    return mat

# Create and assign materials
handle_mat = create_material("Handle", (1, 0, 0, 1))  # Red
texture_mat = create_material("Texture", (0.8, 0.8, 0.8, 1),
                "/home/zaya/Downloads/Workspace/Animations/Textures/Poliigon_BrickWallReclaimed_8320/Poliigon_BrickWallReclaimed_8320_Preview1.png")
upholstery_mat = create_material("Upholstery", (0.6, 0.3, 0.2, 1),
                "/home/zaya/Downloads/Workspace/Animations/Textures/Poliigon_RattanWeave_6945/Poliigon_RattanWeave_6945_Preview1.png")

# Assign materials to object
klein_bottle.data.materials.clear()
klein_bottle.data.materials.append(handle_mat)
klein_bottle.data.materials.append(texture_mat)
klein_bottle.data.materials.append(upholstery_mat)

# ========== ANIMATION SETUP ==========
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 100

# Scale animation
klein_bottle.scale = (1, 1, 1)
klein_bottle.keyframe_insert("scale", frame=1)
klein_bottle.scale = (1.2, 0.8, 1)
klein_bottle.keyframe_insert("scale", frame=30)

# Wave modifier
wave = klein_bottle.modifiers.new("Wave", 'WAVE')
wave.speed = 0.2
wave.width = 0.5
wave.height = 0.1

# ========== LIGHTING ==========
bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
light = bpy.context.object
light.data.energy = 300

# ========== CAMERA SETUP ==========
bpy.ops.object.camera_add(location=(5, -5, 3))
camera = bpy.context.object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))
scene.camera = camera

# ========== RENDER SETTINGS ==========
output_dir = "/home/zaya/Downloads/Workspace/Animations"
os.makedirs(output_dir, exist_ok=True)

scene.render.filepath = os.path.join(output_dir, "klein_")
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'

print(f"Render output will be saved to: {scene.render.filepath}")
print("Setup complete. Ready to render animation.")