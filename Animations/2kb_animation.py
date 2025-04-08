import math
import traceback
import os

import bpy
import mathutils
from mathutils import Euler, Vector


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

        # Path to your 3D object file (replace with your actual path)
        file_path = "/home/zaya/Documents/Gitrepos/kleinsfantasy/models/klein.blend"        

        # Specify the name of the object to link
        object_name = "Circle.002"  # Replace with the actual name of your object in the .blend file

        # Load the .blend file
        with bpy.data.libraries.load(file_path, link=False) as (data_from, data_to):
            if object_name in data_from.objects:
                data_to.objects = [object_name]

        # Link the object to the current scene
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
                klein_bottle = obj
                klein_bottle.location = Vector((0,0,0))
                # klein_bottle.name = "Klein_Bottle"
                print(f"Klein bottle created: {klein_bottle}")
                return klein_bottle

       
    except Exception as e:
        print("Error creating the Klein bottle:", e)
        traceback.print_exc()
        return None

# def apply_materials(klein_bottle):
#     """Apply different materials to the Klein bottle."""
#     try:
#         # Handle material (Red Color)
#         handle_material = bpy.data.materials.new(name="HandleMaterial")
#         handle_material.use_nodes = True
#         klein_bottle.data.materials.append(handle_material)
#         print("Handle material applied.")

#         # Texture Material (Chinese writing texture)
#         texture_material = bpy.data.materials.new(name="TextureMaterial")
#         texture_material.use_nodes = True
#         klein_bottle.data.materials.append(texture_material)
#         print("Texture material applied.")

#         # Set texture
#         nodes = texture_material.node_tree.nodes
#         tex_image = nodes.new(type="ShaderNodeTexImage")
#         tex_image.image = bpy.data.images.load("/home/zaya/Downloads/Workspace/Animations/Textures/Poliigon_BrickWallReclaimed_8320/Poliigon_BrickWallReclaimed_8320_Preview1.png")  # Replace with actual path
#         bsdf = nodes.get("Principled BSDF")
#         if bsdf:
#             texture_material.node_tree.links.new(tex_image.outputs["Color"], bsdf.inputs["Base Color"])

#         # Upholstery Material
#         upholstery_material = bpy.data.materials.new(name="UpholsteryMaterial")
#         upholstery_material.use_nodes = True
#         klein_bottle.data.materials.append(upholstery_material)
#         print("Upholstery material applied.")

#         # Add upholstery texture
#         upholstery_texture = nodes.new(type="ShaderNodeTexImage")
#         upholstery_texture.image = bpy.data.images.load("/home/zaya/Downloads/Workspace/Animations/Textures/Poliigon_RattanWeave_6945/Poliigon_RattanWeave_6945_Preview1.png")  # Replace with actual path
#         if bsdf:
#             upholstery_material.node_tree.links.new(upholstery_texture.outputs["Color"], bsdf.inputs["Base Color"])

#     except Exception as e:
#         print("Error applying materials:", e)
#         traceback.print_exc()


def duplicate_klein_bottle(klein_bottle):
    """Duplicate the Klein bottle to set up interaction with debugging."""
    try:
        bottle1 = klein_bottle
        bottle2 = klein_bottle.copy()
        bottle2.location = (20, 10, 10)
        bpy.context.collection.objects.link(bottle2)
        print(f"Klein bottle duplicated: bottle1 at (0, 0, 0), bottle2 at (3, 0, 0).")
        return bottle1, bottle2
    except Exception as e:
        print("Error duplicating Klein bottle:", e)
        traceback.print_exc()
        return None, None


def rotate_obj(obj, rotations=4, start_frame=1, end_frame=120):
    """Rotates an object multiple times around Z-axis with smooth easing."""
    try:
        # Clear existing rotation animations
        obj.rotation_euler = (0, 0, 0)
        obj.keyframe_insert(data_path="rotation_euler", frame=start_frame)
        
        # Calculate total rotation (4 full rotations = 4*2π radians)
        total_rotation = rotations * 2 * math.pi
        
        # Set rotation with easing for smooth start/stop
        obj.rotation_euler = Euler((0, 0, total_rotation), 'XYZ')
        obj.keyframe_insert(data_path="rotation_euler", frame=end_frame)
        
        # Apply smooth interpolation to rotation
        for fcurve in obj.animation_data.action.fcurves:
            if fcurve.data_path == "rotation_euler":
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'BEZIER'
                    keyframe.easing = 'AUTO'
        
        print(f"{obj.name} set to rotate {rotations} times from frame {start_frame}-{end_frame}")
        return True
        
    except Exception as e:
        print(f"Error animating {obj.name} rotation:", e)
        traceback.print_exc()
        return False

def animate_interaction(bottle1, bottle2):
    """Enhanced interaction animation with coordinated movement."""
    # Animation parameters
    start_frame = 1
    mid_frame = 60
    end_frame = 120
    height = 3.0  # Peak jump height
    
    # Bottle 1 animation (circular arc with rotation)
    bottle1.location = (0, 0, 0)
    bottle1.keyframe_insert("location", frame=start_frame)
    
    bottle1.location = (2, 2, height)
    bottle1.keyframe_insert("location", frame=mid_frame)
    
    bottle1.location = (4, 0, 0)
    bottle1.keyframe_insert("location", frame=end_frame)
    
    # Bottle 2 animation (opposite movement)
    bottle2.location = (4, 0, 0)
    bottle2.keyframe_insert("location", frame=start_frame)
    
    bottle2.location = (2, -2, height)
    bottle2.keyframe_insert("location", frame=mid_frame)
    
    bottle2.location = (0, 0, 0)
    bottle2.keyframe_insert("location", frame=end_frame)
    
    # Add rotation to both bottles
    rotate_obj(bottle1, rotations=4, start_frame=start_frame, end_frame=end_frame)
    rotate_obj(bottle2, rotations=-4, start_frame=start_frame, end_frame=end_frame)  # Reverse rotation
    
    # Smooth all location animations
    for obj in [bottle1, bottle2]:
        if obj.animation_data:
            for fcurve in obj.animation_data.action.fcurves:
                if fcurve.data_path == "location":
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'
    
    print(f"Interaction animation complete (frames {start_frame}-{end_frame})")
    return True
        

def setup_camera(bottle1, bottle2):
    """Smart camera setup that tracks midpoint between two objects with dynamic framing."""
    try:
        import mathutils
        from mathutils import Vector

        # Clear existing cameras
        for obj in bpy.data.objects:
            if obj.type == 'CAMERA':
                bpy.data.objects.remove(obj, do_unlink=True)

        # Create tracking empty
        midpoint_empty = bpy.data.objects.get("Midpoint")
        if not midpoint_empty:
            midpoint_empty = bpy.data.objects.new("Midpoint", None)
            bpy.context.collection.objects.link(midpoint_empty)

        # Initial camera position (will be adjusted)
        bpy.ops.object.camera_add(location=(0, -85, 50))
        camera = bpy.context.object
        camera.data.lens = 35  # Wider angle than 50mm for better framing
        camera.data.clip_start = 0.1  # Prevent near-clip issues
        camera.data.clip_end = 1000   # Ensure far objects are visible

        # Add tracking constraint
        track_constraint = camera.constraints.new('TRACK_TO')
        track_constraint.target = midpoint_empty
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_constraint.up_axis = 'UP_Y'

        # Animation settings
        start_frame = bpy.context.scene.frame_start
        end_frame = bpy.context.scene.frame_end
        keyframe_step = 30  # Adjust tracking every N frames

        print(f"Setting up camera tracking from frame {start_frame} to {end_frame}")

        for frame in range(start_frame, end_frame + 1, keyframe_step):
            bpy.context.scene.frame_set(frame)
            
            # Get current bottle positions
            bottle1_pos = bottle1.matrix_world.translation
            bottle2_pos = bottle2.matrix_world.translation
            
            # Calculate dynamic midpoint
            midpoint = (bottle1_pos + bottle2_pos) / 2
            midpoint_empty.location = midpoint
            
            # Calculate automatic camera distance (2x object separation)
            obj_distance = (bottle1_pos - bottle2_pos).length
            cam_distance = max(10, obj_distance * 12.5)  # Minimum 10 units
            
            # Set camera position in an arc
            angle = math.radians(45)  # 45 degree elevation
            camera.location = midpoint + Vector((
                -cam_distance * math.cos(angle),
                -cam_distance * math.sin(angle),
                cam_distance * 0.7  # Slightly higher than midpoint
            ))
            
            # Keyframe everything
            midpoint_empty.keyframe_insert("location", frame=frame)
            camera.keyframe_insert("location", frame=frame)
            
            # Debug output
            if frame == start_frame:
                print(f"Initial camera position: {camera.location}")
                print(f"Tracking midpoint at: {midpoint}")

        bpy.context.scene.camera = camera
        print("Camera setup complete with dynamic tracking")
        return camera

    except Exception as e:
        print("Camera setup error:", str(e))
        traceback.print_exc()
        return None

def setup_render_settings():
    """Configure render settings for quick 5-second output with Eevee."""
    try:
        scene = bpy.context.scene
        
        # Set animation length to 5 seconds (120 frames at 24fps)
        scene.frame_start = 1
        scene.frame_end = 120
        scene.render.fps = 24
        
        # Use Eevee for faster rendering
        scene.render.engine = 'BLENDER_EEVEE'
        
        # Resolution settings
        scene.render.resolution_x = 1280
        scene.render.resolution_y = 720
        scene.render.resolution_percentage = 100  # Full resolution
        
        # Eevee quality settings
        scene.eevee.taa_render_samples = 32
        scene.eevee.use_gtao = True
        scene.eevee.use_bloom = True
        
        # Output settings
        output_dir = "/home/zaya/Downloads/Workspace/Animations/MP4"
        os.makedirs(output_dir, exist_ok=True)
        scene.render.filepath = os.path.join(output_dir, "5s_klein_animation.mp4")
        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.codec = 'H264'
        scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'

        print("Render settings configured for quick 5-second animation.")
        return True
    except Exception as e:
        print("Error setting render settings:", e)
        traceback.print_exc()
        return False

def apply_materials(obj):
    """Apply materials with proper error handling."""
    try:
        # Clear existing materials
        obj.data.materials.clear()
        
        # Create handle material (red)
        handle_mat = bpy.data.materials.new(name="HandleMaterial")
        handle_mat.use_nodes = True
        bsdf = handle_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (1, 0, 0, 1)  # Red
        obj.data.materials.append(handle_mat)
        
        # Create texture material
        texture_mat = bpy.data.materials.new(name="TextureMaterial")
        texture_mat.use_nodes = True
        nodes = texture_mat.node_tree.nodes
        links = texture_mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        tex_image = nodes.new(type="ShaderNodeTexImage")
        output = nodes.new(type='ShaderNodeOutputMaterial')
        
        try:
            tex_image.image = bpy.data.images.load(
                "/home/zaya/Downloads/Workspace/Animations/Textures/Poliigon_BrickWallReclaimed_8320/Poliigon_BrickWallReclaimed_8320_Preview1.png"
            )
        except:
            print("Brick texture not found, using default color")
            bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
        else:
            links.new(tex_image.outputs["Color"], bsdf.inputs["Base Color"])
        
        links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
        obj.data.materials.append(texture_mat)
        
        # Create upholstery material
        upholstery_mat = bpy.data.materials.new(name="UpholsteryMaterial")
        upholstery_mat.use_nodes = True
        nodes = upholstery_mat.node_tree.nodes
        links = upholstery_mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.inputs["Base Color"].default_value = (0.6, 0.3, 0.2, 1)  # Brown
        output = nodes.new(type='ShaderNodeOutputMaterial')
        
        try:
            tex_image = nodes.new(type="ShaderNodeTexImage")
            tex_image.image = bpy.data.images.load(
                "/home/zaya/Downloads/Workspace/Animations/Textures/Poliigon_RattanWeave_6945/Poliigon_RattanWeave_6945_Preview1.png"
            )
            links.new(tex_image.outputs["Color"], bsdf.inputs["Base Color"])
        except:
            print("Rattan texture not found, using default color")
        
        links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
        obj.data.materials.append(upholstery_mat)
        
        print("All materials applied successfully")
        return True
        
    except Exception as e:
        print(f"Material error: {str(e)}")
        traceback.print_exc()
        return False

# def setup_camera(bottle1, bottle2):
#     """Camera setup that always works."""
#     try:
#         # Remove existing cameras
#         for obj in bpy.data.objects:
#             if obj.type == 'CAMERA':
#                 bpy.data.objects.remove(obj)
        
#         # Create camera
#         bpy.ops.object.camera_add(location=(0, -85, 15))
#         camera = bpy.context.object
#         camera.data.lens = 35
        
#         # Point camera between bottles
#         loc1 = bottle1.location
#         loc2 = bottle2.location
#         midpoint = ((loc1.x + loc2.x)/2, 
#                    (loc1.y + loc2.y)/2, 
#                    (loc1.z + loc2.z)/2)
        
#         # Create empty for tracking
#         if "CameraTarget" not in bpy.data.objects:
#             bpy.ops.object.empty_add(location=midpoint)
#             target = bpy.context.object
#             target.name = "CameraTarget"
#         else:
#             target = bpy.data.objects["CameraTarget"]
#             target.location = midpoint
        
#         # Add tracking constraint
#         track = camera.constraints.new(type='TRACK_TO')
#         track.target = target
#         track.track_axis = 'TRACK_NEGATIVE_Z'
#         track.up_axis = 'UP_Y'
        
#         bpy.context.scene.camera = camera
#         print("Camera setup complete")
#         return True
        
#     except Exception as e:
#         print(f"Camera error: {str(e)}")
#         traceback.print_exc()
#         return False

def main():
    print("Starting animation setup...")
    
    # 1. Clear scene
    clear_scene()
    
    # 2. Setup render settings first
    if not setup_render_settings():
        return
    
    # 3. Create base object
    klein_bottle = create_klein_bottle()
    if not klein_bottle:
        return
    
    # 4. Apply materials
    if not apply_materials(klein_bottle):
        return  # Continue even if materials fail
    
    # 5. Duplicate and animate
    bottle1, bottle2 = duplicate_klein_bottle(klein_bottle)
    if not bottle1 or not bottle2:
        return
    
    if not animate_interaction(bottle1, bottle2):
        return
    
    # 6. Setup camera (critical)
    if not setup_camera(bottle1, bottle2):
        return
    
    print("All systems ready for rendering!")
    print("Run: blender --background --python your_script.py --render-anim")

if __name__ == "__main__":
    main()