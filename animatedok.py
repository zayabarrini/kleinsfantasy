import math
import traceback

import bpy
from mathutils import Vector


def clear_scene():
    """Clear the existing scene objects."""
    try:
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        print("Scene cleared.")
    except Exception as e:
        print("Error clearing the scene:", e)
        traceback.print_exc()

def create_klein_bottle():
    """Create an approximation of a Klein bottle using a torus."""
    try:
        print("Creating torus as base for Klein bottle...")
        bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.3, major_segments=48, minor_segments=12)
        klein_bottle = bpy.context.object
        klein_bottle.name = "Klein_Bottle"
       
        print(f"Klein bottle created: {klein_bottle}")
        return klein_bottle
    except Exception as e:
        print("Error creating the Klein bottle:", e)
        traceback.print_exc()
        return None

def apply_materials(klein_bottle):
    """Apply different materials to the Klein bottle."""
    try:
        # Handle material (Red Color)
        handle_material = bpy.data.materials.new(name="HandleMaterial")
        handle_material.use_nodes = True
        klein_bottle.data.materials.append(handle_material)
        print("Handle material applied.")

        # Texture Material (Chinese writing texture)
        texture_material = bpy.data.materials.new(name="TextureMaterial")
        texture_material.use_nodes = True
        klein_bottle.data.materials.append(texture_material)
        print("Texture material applied.")

        # Set texture
        nodes = texture_material.node_tree.nodes
        tex_image = nodes.new(type="ShaderNodeTexImage")
        tex_image.image = bpy.data.images.load("/home/talles/Downloads/Environments/Psychoanalysis/textures/Poliigon_BrickWallReclaimed_8320/Poliigon_BrickWallReclaimed_8320_Preview1.png")  # Replace with actual path
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            texture_material.node_tree.links.new(tex_image.outputs["Color"], bsdf.inputs["Base Color"])

        # Upholstery Material
        upholstery_material = bpy.data.materials.new(name="UpholsteryMaterial")
        upholstery_material.use_nodes = True
        klein_bottle.data.materials.append(upholstery_material)
        print("Upholstery material applied.")

        # Add upholstery texture
        upholstery_texture = nodes.new(type="ShaderNodeTexImage")
        upholstery_texture.image = bpy.data.images.load("/home/talles/Downloads/Environments/Psychoanalysis/textures/Poliigon_RattanWeave_6945/Poliigon_RattanWeave_6945_Preview1.png")  # Replace with actual path
        if bsdf:
            upholstery_material.node_tree.links.new(upholstery_texture.outputs["Color"], bsdf.inputs["Base Color"])

    except Exception as e:
        print("Error applying materials:", e)
        traceback.print_exc()

def animate_klein_bottle(klein_bottle):
    """Animate the Klein bottle with scaling and wave motion."""
    try:
        # Initial scale keyframe
        print("Animating Klein bottle scale...")
        klein_bottle.scale = (1, 1, 1)
        klein_bottle.keyframe_insert(data_path="scale", frame=1)
        print("Initial scale keyframe set.")

        # Set a second scale keyframe with modified proportions
        klein_bottle.scale = (1.2, 0.8, 1)
        klein_bottle.keyframe_insert(data_path="scale", frame=30)
        print("Second scale keyframe set.")

        # Apply wave modifier for a wavy effect
        print("Applying wave modifier...")
        modifier = klein_bottle.modifiers.new(name="Wave", type='WAVE')
        modifier.speed = 0.2
        modifier.width = 0.5
        modifier.height = 0.1
        print("Wave modifier applied with speed 0.2, width 0.5, and height 0.1.")

        # Set animation frames
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 100
        print("Animation frames set from 1 to 100.")

    except Exception as e:
        print("Error animating Klein bottle:", e)
        traceback.print_exc()

def add_light():
    """Add a light source to the scene with debugging."""
    try:
        bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
        light = bpy.context.object
        light.data.energy = 300
        print("Light added at location (5, -5, 5) with energy 300.")
        return light
    except Exception as e:
        print("Error adding light:", e)
        traceback.print_exc()
        return None

def duplicate_klein_bottle(klein_bottle):
    """Duplicate the Klein bottle to set up interaction with debugging."""
    try:
        bottle1 = klein_bottle
        bottle2 = klein_bottle.copy()
        bottle2.location = (3, 0, 0)
        bpy.context.collection.objects.link(bottle2)
        print(f"Klein bottle duplicated: bottle1 at (0, 0, 0), bottle2 at (3, 0, 0).")
        return bottle1, bottle2
    except Exception as e:
        print("Error duplicating Klein bottle:", e)
        traceback.print_exc()
        return None, None

def animate_interaction(bottle1, bottle2):
    """Animate interaction between two bottles with keyframe insertion."""
    try:
        bottle1.location = (0, 0, 0)
        bottle1.keyframe_insert(data_path="location", frame=1)
        bottle1.location = (1, 1, 0)
        bottle1.keyframe_insert(data_path="location", frame=50)
        print("Bottle1 keyframes set from (0, 0, 0) to (1, 1, 0).")

        bottle2.location = (3, 0, 0)
        bottle2.keyframe_insert(data_path="location", frame=1)
        bottle2.location = (2, 1, 0)
        bottle2.keyframe_insert(data_path="location", frame=50)
        print("Bottle2 keyframes set from (3, 0, 0) to (2, 1, 0).")

    except Exception as e:
        print("Error setting up interaction animation:", e)
        traceback.print_exc()

def apply_costume_with_holes(material):
    """Apply costume material with clipping for holes."""
    try:
        if material.use_nodes:
            node_tree = material.node_tree
            bsdf = node_tree.nodes.get("Principled BSDF")
            texture = node_tree.nodes.get("Image Texture")
            if bsdf and texture:
                texture.extension = 'CLIP'  # Clip texture for holes
                print(f"Clipping applied on material: {material.name}")
            else:
                print("Warning: Required nodes not found in material.")
        else:
            print("Material does not use nodes; skipping hole application.")
    except Exception as e:
        print(f"Error applying costume with holes to material: {material.name}")
        traceback.print_exc()

def setup_camera():
    """Add a camera and set its properties with debugging."""
    try:
        bpy.ops.object.camera_add(location=(5, -5, 3))
        camera = bpy.context.object
        bpy.context.scene.camera = camera
        camera.rotation_euler = (math.radians(60), 0, math.radians(45))
        print("Camera added at location (5, -5, 3) with rotation (60°, 0, 45°).")
    except Exception as e:
        print("Error setting up camera:", e)
        traceback.print_exc()

def setup_render_settings():
    """Configure render settings for output with debugging."""
    try:
        bpy.context.scene.render.filepath = "/home/talles/Downloads/Environments/Psychoanalysis/animations/klein"
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = 'MPEG4'
        bpy.context.scene.render.ffmpeg.codec = 'H264'
        bpy.ops.render.render(animation=True)
        print("Render settings configured: Filepath set to /home/talles/Downloads/Environments/Psychoanalysis/animations/klein.MPEG4.")
    except Exception as e:
        print("Error setting render settings:", e)
        traceback.print_exc()

def main():
    print("Starting Klein bottle interaction setup with animations and textures...")
    clear_scene()

    klein_bottle = create_klein_bottle()
    if klein_bottle:
        apply_materials(klein_bottle)
        animate_klein_bottle(klein_bottle)
    else:
        print("Failed to create Klein bottle; skipping material application and animation.")

    print("Script finished.")

    if klein_bottle:
        add_light()
        bottle1, bottle2 = duplicate_klein_bottle(klein_bottle)
        
        if bottle1 and bottle2:
            animate_interaction(bottle1, bottle2)
        
        # Apply textures with clipping holes
        for material_name in ["HandleMaterial", "TextureMaterial", "UpholsteryMaterial"]:
            material = bpy.data.materials.get(material_name)
            if material:
                apply_costume_with_holes(material)
            else:
                print(f"Warning: Material '{material_name}' not found.")

        # setup_camera()
        # setup_render_settings()
        
        print("Setup complete. Run the animation in Blender to see the results.")
    else:
        print("Failed to create Klein bottle; exiting script.")
   
# Run the script
main()

