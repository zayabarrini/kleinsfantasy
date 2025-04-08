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

# Create and assign materials (simplified for quick render)
handle_mat = create_material("Handle", (1, 0, 0, 1))  # Red
klein_bottle.data.materials.clear()
klein_bottle.data.materials.append(handle_mat)

# ========== ANIMATION SETUP ==========
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 125  # 5 seconds at 25 fps

# Rotation animation
klein_bottle.rotation_euler = (0, 0, 0)
klein_bottle.keyframe_insert("rotation_euler", frame=1)
klein_bottle.rotation_euler = (math.radians(360), 0, 0)
klein_bottle.keyframe_insert("rotation_euler", frame=125)

# Simple scale animation
klein_bottle.scale = (1, 1, 1)
klein_bottle.keyframe_insert("scale", frame=1)
klein_bottle.scale = (1.2, 1.2, 1.2)
klein_bottle.keyframe_insert("scale", frame=63)
klein_bottle.scale = (1, 1, 1)
klein_bottle.keyframe_insert("scale", frame=125)

# ========== LIGHTING ==========
bpy.ops.object.light_add(type='SUN', location=(5, -5, 5))
light = bpy.context.object
light.data.energy = 5  # Lower energy for Sun type

# ========== CAMERA SETUP ==========
bpy.ops.object.camera_add(location=(5, -5, 3))
camera = bpy.context.object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))
scene.camera = camera

# ========== RENDER SETTINGS ==========
output_dir = "/home/zaya/Downloads/Workspace/Animations/MP4"
os.makedirs(output_dir, exist_ok=True)

scene.render.filepath = os.path.join(output_dir, "animated_klein.mp4")
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS'

# Optimize for quick rendering
scene.render.engine = 'BLENDER_EEVEE'  # Faster than Cycles
scene.render.resolution_x = 1280  # Lower resolution
scene.render.resolution_y = 720
scene.render.fps = 25  # Standard film fps
scene.eevee.taa_render_samples = 16  # Lower samples
scene.eevee.use_gtao = True  # Enable ambient occlusion
scene.eevee.use_bloom = True  # Enable bloom for better look

# Remove unnecessary passes
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'

print(f"Render output will be saved to: {scene.render.filepath}")
print("Setup complete. Ready to render animation.")