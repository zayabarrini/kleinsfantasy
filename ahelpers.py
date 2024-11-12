# Merged and cleaned Python file
import contextlib
import datetime
import functools
import json
import logging
import math
import os
import pathlib
import pprint
import random
import shutil
import time
from datetime import datetime

import addon_utils
import bpy
import mathutils
from bpybb.hdri import apply_hdri
from bpybb.material import apply_material, make_color_ramp_from_color_list
from bpybb.object import apply_location, track_empty
from bpybb.output import set_1080px_square_render_res
from bpybb.random import time_seed
from bpybb.utils import active_object, clean_scene

# Function list:
# - purge_orphans
# - clean_scene
# - active_object
# - time_seed
# - set_fcurve_extrapolation_to_linear
# - create_data_animation_loop
# - set_scene_props
# - scene_setup
# - link_nodes_by_mesh_socket
# - create_node
# - create_random_bool_value_node
# - create_separate_geo_node
# - create_scale_element_geo_node
# - separate_faces_and_animate_scale
# - update_geo_node_tree
# - create_centerpiece
# - main
# - get_random_pallet_color
# - add_ctrl_empty
# - setup_camera
# - set_scene_props
# - get_color_palette
# - setup_scene
# - add_lights
# - gen_base_material
# - setup_material
# - gen_perlin_curve
# - add_shape_key
# - create_bevel_object
# - animate_curve
# - gen_scene
# - gen_centerpiece
# - main
# - purge_orphans
# - clean_scene
# - active_object
# - add_ctrl_empty
# - make_active
# - set_fcurve_extrapolation_to_linear
# - animate_360_rotation
# - animate_rotation
# - set_1080p_render_res
# - set_scene_props
# - remove_libraries
# - get_script_path
# - get_script_folder_path
# - scene_setup
# - create_light_rig
# - get_working_directory_path
# - get_list_of_blend_files
# - link_objects
# - create_floor
# - prepare_scene
# - get_object_center
# - focus_camera_on_target_obj
# - update_scene
# - run_turntable_render
# - unlink_objects
# - render_turntable_models
# - main
# - purge_orphans
# - clean_scene
# - active_object
# - time_seed
# - add_ctrl_empty
# - apply_material
# - make_active
# - track_empty
# - setup_camera
# - create_detail_rotation
# - set_1080px_square_render_res
# - set_scene_props
# - setup_scene
# - make_spline_fcurve_interpolation_linear
# - get_random_color
# - render_loop
# - enable_extra_curves
# - create_emissive_material
# - create_metal_material
# - add_lights
# - create_profile_curve
# - create_base_curve
# - animate_point_tilt
# - create_primary_curve
# - create_emissive_curve
# - create_centerpiece
# - main
# - purge_orphans
# - clean_scene
# - active_object
# - time_seed
# - add_ctrl_empty
# - make_active
# - track_empty
# - setup_camera
# - set_1080px_square_render_res
# - set_scene_props
# - setup_scene
# - make_fcurves_linear
# - get_random_color
# - apply_material
# - add_lights
# - create_circle_control_empty
# - animate_object_translation
# - gen_centerpiece
# - main
# - purge_orphans
# - clean_scene
# - clean_scene_experimental
# - active_object
# - time_seed
# - add_empty
# - make_active
# - track_empty
# - set_1080px_square_render_res
# - hex_color_to_rgb
# - hex_color_to_rgba
# - convert_srgb_to_linear_rgb
# - create_data_animation_loop
# - parent
# - apply_material
# - set_fcurve_extrapolation_to_linear
# - apply_hdri
# - animate_360_rotation
# - animate_rotation
# - enable_extra_curves
# - setup_camera
# - set_scene_props
# - scene_setup
# - add_lights
# - render_loop
# - create_metallic_material
# - get_random_color
# - create_bevel_obj
# - add_curve
# - create_centerpiece
# - main
# - purge_orphans
# - clean_scene
# - active_object
# - time_seed
# - add_ctrl_empty
# - apply_material
# - make_active
# - track_empty
# - setup_camera
# - create_detail_rotation
# - set_1080px_square_render_res
# - set_scene_props
# - setup_scene
# - make_spline_fcurve_interpolation_linear
# - get_random_color
# - render_loop
# - enable_extra_curves
# - create_emissive_material
# - create_metal_material
# - apply_hdri
# - add_lights
# - create_profile_curve
# - create_base_curve
# - animate_point_tilt
# - create_primary_curve
# - create_emissive_curve
# - create_centerpiece
# - main
# - purge_orphans
# - clean_scene
# - hex_color_to_rgb
# - hex_color_to_rgba
# - convert_srgb_to_linear_rgb
# - active_object
# - time_seed
# - add_ctrl_empty
# - make_active
# - track_empty
# - setup_camera
# - set_1080px_square_render_res
# - set_scene_props
# - scene_setup
# - make_fcurves_bounce
# - render_loop
# - get_random_color
# - get_random_highlight_color
# - add_lights
# - create_metallic_material
# - apply_material
# - animate_rotation
# - create_bevel
# - create_centerpiece
# - main
# - purge_orphans
# - clean_scene
# - clean_scene_experimental
# - active_object
# - time_seed
# - add_ctrl_empty
# - make_active
# - track_empty
# - set_1080px_square_render_res
# - set_fcurve_extrapolation_to_linear
# - hex_color_to_rgb
# - hex_color_to_rgba
# - convert_srgb_to_linear_rgb
# - create_base_material
# - render_loop
# - setup_camera
# - set_scene_props
# - scene_setup
# - add_light
# - edit_mode
# - subdivide
# - create_data_animation_loop
# - make_color_ramp_stops_from_colors
# - set_keyframe_point_interpolation_to_elastic
# - create_cast_to_sphere_animation_loop
# - create_mesh_instance
# - create_primary_mesh
# - create_centerpiece
# - get_colors
# - main
# - purge_orphans
# - clean_scene
# - clean_scene_experimental
# - active_object
# - time_seed
# - add_ctrl_empty
# - make_active
# - track_empty
# - set_1080px_square_render_res
# - set_fcurve_extrapolation_to_linear
# - hex_color_to_rgb
# - hex_color_to_rgba
# - convert_srgb_to_linear_rgb
# - animate_360_rotation
# - animate_rotation
# - apply_rotation
# - apply_random_rotation
# - apply_emission_material
# - create_emission_material
# - create_reflective_material
# - apply_reflective_material
# - render_loop
# - get_random_color
# - setup_camera
# - set_scene_props
# - scene_setup
# - add_light
# - apply_glare_composite_effect
# - apply_metaball_material
# - create_metaball_path
# - create_metaball
# - create_centerpiece
# - create_background
# - main
# - purge_orphans
# - clean_scene
# - active_object
# - time_seed
# - add_ctrl_empty
# - apply_material
# - make_active
# - track_empty
# - setup_camera
# - set_1080px_square_render_res
# - make_fcurves_linear
# - get_random_color
# - render_loop
# - create_background
# - create_emissive_ring
# - create_emissive_ring_material
# - create_metal_ring_material
# - create_floor_material
# - create_floor
# - add_light
# - set_scene_props
# - setup_scene
# - animate_rotation
# - create_ring
# - create_centerpiece
# - main
# - purge_orphans
# - clean_scene
# - active_object
# - time_seed
# - add_ctrl_empty
# - make_active
# - track_empty
# - setup_camera
# - set_1k_square_render_res
# - set_scene_props
# - setup_scene
# - make_fcurves_linear
# - get_random_color
# - apply_material
# - add_lights
# - render_loop
# - animate_object_rotation
# - gen_centerpiece
# - gen_background
# - main
# - purge_orphans
# - clean_scene
# - active_object
# - time_seed
# - add_ctrl_empty
# - make_active
# - track_empty
# - setup_camera
# - set_1k_square_render_res
# - set_scene_props
# - setup_scene
# - enable_import_images_as_planes
# - add_light
# - get_list_of_loops
# - get_grid_step
# - gen_centerpiece
# - main
# - clean_sequencer
# - find_sequence_editor
# - get_image_files
# - get_image_dimensions
# - set_up_output_params
# - gen_video_from_images
# - main
# - purge_orphans
# - clean_scene
# - active_object
# - time_seed
# - add_ctrl_empty
# - make_active
# - track_empty
# - setup_camera
# - set_1080px_square_render_res
# - set_scene_props
# - setup_scene
# - make_fcurves_linear
# - get_random_color
# - render_loop
# - apply_random_color_material
# - add_lights
# - loop_param
# - set_keyframe_to_ease_in_out
# - animate_shape
# - create_shape
# - gen_centerpiece
# - main
# - clean_sequencer
# - find_sequence_editor
# - set_up_output_params
# - clean_proxies
# - on_error
# - trim_the_video
# - move_the_clip_into_position
# - apply_fade_in_to_clip
# - create_transition_between_videos
# - main
# - purge_orphans
# - clean_scene
# - clean_scene_experimental
# - active_object
# - time_seed
# - add_ctrl_empty
# - duplicate_object
# - make_active
# - track_empty
# - enable_addon
# - enable_extra_curves
# - join_objects
# - set_1080px_square_render_res
# - set_fcurve_extrapolation_to_linear
# - hex_color_to_rgb
# - hex_color_to_rgba
# - convert_srgb_to_linear_rgb
# - deselect_all_objects
# - create_collection
# - add_to_collection
# - make_instance_of_collection
# - rotate_object
# - create_reflective_material
# - apply_reflective_material
# - set_up_world_sun_light
# - configure_logging
# - load_color_palettes
# - select_random_color_palette
# - get_color_palette
# - get_random_color
# - select_color_pair
# - setup_camera
# - set_scene_props
# - scene_setup
# - animate_truchet_tile
# - create_truchet_tile_pattern
# - create_truchet_tile
# - create_truchet_tile_platform
# - create_truchet_tile_platform_group
# - animate_camera
# - create_and_animate_camera
# - create_centerpiece
# - main
# - time_seed
# - hex_color_str_to_rgba
# - convert_srgb_to_linear_rgb
# - choose_random_color
# - load_color_palettes
# - setup_scene
# - prepare_and_render_scene
# - render_all_palettes
# - update_colors
# - main
# - purge_orphans
# - clean_scene
# - clean_scene_experimental
# - active_object
# - time_seed
# - add_empty
# - make_active
# - track_empty
# - set_1080px_square_render_res
# - set_fcurve_interpolation_to_linear
# - hex_color_to_rgb
# - hex_color_to_rgba
# - convert_srgb_to_linear_rgb
# - duplicate_object
# - enable_addon
# - enable_extra_meshes
# - enable_mod_tools
# - get_random_color
# - setup_camera
# - set_scene_props
# - scene_setup
# - create_metallic_material
# - apply_metallic_material
# - add_lights
# - create_light_rig
# - make_surface
# - update_object
# - animate_object_update
# - create_centerpiece
# - create_background
# - main
# - purge_orphans
# - clean_scene
# - active_object
# - time_seed
# - add_ctrl_empty
# - make_active
# - track_empty
# - setup_camera
# - set_1080px_square_render_res
# - set_scene_props
# - setup_scene
# - hex_color_str_to_rgba
# - convert_srgb_to_linear_rgb
# - load_color_palettes
# - select_random_color_palette
# - create_color_plane
# - create_text_object
# - parent_to_empty
# - create_centerpiece
# - main
# - remove_compositor_nodes
# - get_image_files
# - add_compositor_nodes
# - import_image_sequence_into_compositor
# - main

def purge_orphans():
    """
    Remove all orphan data blocks
    see this from more info:
    https://youtu.be/3rNqVPtbhzc?t=149
    """
    if bpy.app.version >= (3, 0, 0):
        # run this only for Blender versions 3.0 and higher
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    else:
        # run this only for Blender versions lower than 3.0
        # call purge_orphans() recursively until there are no more orphan data blocks to purge
        result = bpy.ops.outliner.orphans_purge()
        if result.pop() != "CANCELLED":
            purge_orphans()

def clean_scene():
    """
    Removing all of the objects, collection, materials, particles,
    textures, images, curves, meshes, actions, nodes, and worlds from the scene
    Checkout this video explanation with example
    "How to clean the scene with Python in Blender (with examples)"
    https://youtu.be/3rNqVPtbhzc
    """
    # make sure the active object is not in Edit Mode
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()
    # make sure non of the objects are hidden from the viewport, selection, or disabled
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False
    # select all the object and delete them (just like pressing A + X + D in the viewport)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    # find all the collections and remove them
    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])
    # in the case when you modify the world shader
    # delete and recreate the world object
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]
    purge_orphans()

def active_object():
    """
    returns the active object
    """
    return bpy.context.active_object

def set_1080px_square_render_res():
    """
    Set the resolution of the rendered image to 1080 by 1080
    """
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080

def subdivide(number_cuts=1, smoothness=0):
    with edit_mode():
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.subdivide(number_cuts=number_cuts, smoothness=smoothness)

def set_1080px_square_render_res():
    """
    Set the resolution of the rendered image to 1080 by 1080
    """
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080

def set_scene_props(fps, loop_seconds):
    """
    Set scene properties
    """
    frame_count = fps * loop_seconds
    scene = bpy.context.scene
    scene.frame_end = frame_count
    # set the world background to black
    world = bpy.data.worlds["World"]
    if "Background" in world.node_tree.nodes:
        world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
    scene.render.fps = fps
    scene.frame_current = 1
    scene.frame_start = 1
    scene.render.engine = "CYCLES"
    # Use the GPU to render
    scene.cycles.device = "GPU"
    # Use the CPU to render
    # scene.cycles.device = "CPU"
    scene.cycles.samples = 300
    scene.view_settings.look = "Very High Contrast"
    set_1080px_square_render_res()

def scene_setup():
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds
    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()
    clean_scene()
    set_scene_props(fps, frame_count)

def link_nodes_by_mesh_socket(node_tree, from_node, to_node):
    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Mesh"])

def create_node(node_tree, type_name, node_x_location, node_location_step_x=0, node_y_location=0):
    """Creates a node of a given type, and sets/updates the location of the node on the X axis.
    Returning the node object and the next location on the X axis for the next node.
    """
    node_obj = node_tree.nodes.new(type=type_name)
    node_obj.location.x = node_x_location
    node_obj.location.y = node_y_location
    node_x_location += node_location_step_x
    return node_obj, node_x_location

def create_random_bool_value_node(node_tree, node_x_location, node_y_location):
    separate_geo_random_value_node, node_x_location = create_node(node_tree, "FunctionNodeRandomValue", node_x_location, node_y_location=node_y_location)
    target_output_type = "BOOLEAN"
    separate_geo_random_value_node.data_type = target_output_type
    random_value_node_output_lookup = {socket.type: socket for socket in separate_geo_random_value_node.outputs.values()}
    target_output_socket = random_value_node_output_lookup[target_output_type]
    return target_output_socket

def create_separate_geo_node(node_tree, node_x_location, node_location_step_x):
    random_value_node_output_socket = create_random_bool_value_node(node_tree, node_x_location, node_y_location=-200)
    separate_geometry_node, node_x_location = create_node(node_tree, "GeometryNodeSeparateGeometry", node_x_location, node_location_step_x)
    separate_geometry_node.domain = "FACE"
    to_node = separate_geometry_node
    node_tree.links.new(random_value_node_output_socket, to_node.inputs["Selection"])
    return separate_geometry_node, node_x_location

def create_scale_element_geo_node(node_tree, geo_selection_node_output, node_x_location, node_y_location):
    random_value_node_output_socket = create_random_bool_value_node(node_tree, node_x_location, node_y_location=node_y_location - 200)
    scale_elements_node, node_x_location = create_node(node_tree, "GeometryNodeScaleElements", node_x_location, node_y_location=node_y_location)
    scale_elements_node.inputs["Scale"].default_value = 0.8
    start_frame = random.randint(0, 150)
    create_data_animation_loop(
        scale_elements_node.inputs["Scale"],
        "default_value",
        start_value=0.0,
        mid_value=0.8,
        start_frame=start_frame,
        loop_length=90,
        linear_extrapolation=False,
    )
    to_node = scale_elements_node
    node_tree.links.new(random_value_node_output_socket, to_node.inputs["Selection"])
    to_node = scale_elements_node
    node_tree.links.new(geo_selection_node_output, to_node.inputs["Geometry"])
    return scale_elements_node

def separate_faces_and_animate_scale(node_tree, node_x_location, node_location_step_x):
    separate_geometry_node, node_x_location = create_separate_geo_node(node_tree, node_x_location, node_location_step_x)
    scale_elements_geo_nodes = []
    top_scale_elements_node = create_scale_element_geo_node(node_tree, separate_geometry_node.outputs["Selection"], node_x_location, node_y_location=200)
    scale_elements_geo_nodes.append(top_scale_elements_node)
    bottom_scale_elements_node = create_scale_element_geo_node(node_tree, separate_geometry_node.outputs["Inverted"], node_x_location, node_y_location=-200)
    scale_elements_geo_nodes.append(bottom_scale_elements_node)
    for fcurve in node_tree.animation_data.action.fcurves.values():
        fcurve.modifiers.new(type="CYCLES")
    node_x_location += node_location_step_x
    join_geometry_node, node_x_location = create_node(node_tree, "GeometryNodeJoinGeometry", node_x_location, node_location_step_x)
    for node in scale_elements_geo_nodes:
        from_node = node
        to_node = join_geometry_node
        node_tree.links.new(from_node.outputs["Geometry"], to_node.inputs["Geometry"])
    return separate_geometry_node, join_geometry_node, node_x_location

def parent_to_empty(text_obj, plane_obj, name):
    empty_obj = add_ctrl_empty(name)
    text_obj.parent = empty_obj
    plane_obj.parent = empty_obj
    return empty_obj
    

def main():
    """
    Python code to import a folder with png(s) into the compositor as a sequence of images.
    """
    image_folder_path = str(pathlib.Path.home() / "tmp" / "my_project")
    fps = 30
    import_image_sequence_into_compositor(image_folder_path, fps)
if __name__ == "__main__":
    main()

def time_seed():
    """
    Sets the random seed based on the time
    and copies the seed into the clipboard
    """
    seed = time.time()
    print(f"seed: {seed}")
    random.seed(seed)
    # add the seed value to your clipboard
    bpy.context.window_manager.clipboard = str(seed)
    return seed

def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")
    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty
    return empty

def select_random_color_palette():
    random_palette = random.choice(load_color_palettes())
    print("Random palette:")
    pprint.pprint(random_palette)
    return random_palette
@functools.cache

def set_scene_props(fps, loop_seconds):
    """
    Set scene properties
    """
    frame_count = fps * loop_seconds
    scene = bpy.context.scene
    scene.frame_end = frame_count
    # set the world background to black
    world = bpy.data.worlds["World"]
    if "Background" in world.node_tree.nodes:
        world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
    scene.render.fps = fps
    scene.frame_current = 1
    scene.frame_start = 1
    scene.eevee.use_bloom = True
    scene.eevee.bloom_intensity = 0.005
    # set Ambient Occlusion properties
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 4
    scene.eevee.gtao_factor = 5
    scene.eevee.taa_render_samples = 64
    scene.view_settings.look = "Very High Contrast"
    set_1080px_square_render_res()

def apply_metallic_material(color, name=None, roughness=0.1):
    material = create_metallic_material(color, name=name, roughness=roughness)
    obj = active_object()
    obj.data.materials.append(material)

def add_lights(context):
    """
    I used this HDRI: https://hdrihaven.com/hdri/?h=dresden_station_night
    Please consider supporting hdrihaven.com @ https://www.patreon.com/polyhaven/overview
    """
    # update the path to where you downloaded the hdri (this will work on Linux, and macOS as well)
    path_to_image = r"C:\tmp\dresden_station_night_1k.exr"
    # Uncomment the next 2 lines for a Linux/macOS path to the HDRI in '~/tmp' folder
    # import os
    # path_to_image = f"{os.path.expanduser('~')}/tmp/dresden_station_night_1k.exr"
    color = get_random_pallet_color(context)
    apply_hdri(path_to_image, bg_color=color, hdri_light_strength=1, bg_strength=1)

def gen_base_material():
    # create new material and enable nodes
    material = bpy.data.materials.new(name="base_material")
    material.use_nodes = True
    # remove all nodes from the material
    nodes_to_remove = []
    for node in material.node_tree.nodes:
        nodes_to_remove.append(node)
    for node in nodes_to_remove:
        material.node_tree.nodes.remove(node)
    location_x = 0
    # create the Texture Coordinate node
    texture_coordinate_node = material.node_tree.nodes.new(type="ShaderNodeTexCoord")
    texture_coordinate_node.location.x = location_x
    location_x += 250
    # create the Mapping node
    mapping_node = material.node_tree.nodes.new(type="ShaderNodeMapping")
    mapping_node.inputs["Rotation"].default_value.y = math.radians(90)
    mapping_node.inputs["Scale"].default_value.z = 0.1
    mapping_node.location.x = location_x
    location_x += 250
    # create the Gradient Texture node
    gradient_texture_node = material.node_tree.nodes.new(type="ShaderNodeTexGradient")
    gradient_texture_node.location.x = location_x
    location_x += 250
    # create the Color Ramp node
    color_ramp_node = material.node_tree.nodes.new(type="ShaderNodeValToRGB")
    color_ramp_node.location.x = location_x
    location_x += 350
    # create the Principled BSDF node
    principled_bsdf_node = material.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
    principled_bsdf_node.location.x = location_x
    location_x += 350
    # create the Material Output node
    material_output_node = material.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
    material_output_node.location.x = location_x
    # setup node links
    material.node_tree.links.new(principled_bsdf_node.outputs["BSDF"], material_output_node.inputs["Surface"])
    material.node_tree.links.new(color_ramp_node.outputs["Color"], principled_bsdf_node.inputs["Base Color"])
    material.node_tree.links.new(mapping_node.outputs["Vector"], gradient_texture_node.inputs["Vector"])
    material.node_tree.links.new(texture_coordinate_node.outputs["Object"], mapping_node.inputs["Vector"])
    material.node_tree.links.new(gradient_texture_node.outputs["Color"], color_ramp_node.inputs["Fac"])
    return material

def setup_material(context):
    material = gen_base_material()
    nodes = material.node_tree.nodes
    make_color_ramp_from_color_list(context["colors"], nodes["ColorRamp"].color_ramp)
    return material

def gen_perlin_curve(context, random_location, current_z):
    bpy.ops.mesh.primitive_circle_add(vertices=512, radius=context["radius"], location=(0, 0, current_z))
    circle = active_object()
    apply_location()
    deform_coords = []
    for vert in circle.data.vertices:
        new_location = vert.co + random_location
        noise_value = mathutils.noise.noise(new_location)
        noise_value = noise_value / 2
        projected_co = mathutils.Vector((vert.co.x, vert.co.y, 0))
        deform_vector = projected_co * noise_value
        deform_coord = vert.co + deform_vector
        deform_coords.append(deform_coord)
    bpy.ops.object.convert(target="CURVE")
    curve_obj = active_object()
    apply_material(context["material"])
    bpy.ops.object.shade_flat()
    curve_obj.data.bevel_mode = "OBJECT"  # remove this for Blender 2.8
    curve_obj.data.bevel_object = context["bevel object"]
    shape_key = add_shape_key(curve_obj, deform_coords)
    return shape_key

def add_shape_key(curve_obj, deform_coords):
    curve_obj.shape_key_add(name="Basis")
    shape_key = curve_obj.shape_key_add(name="Deform")
    deform_coords.reverse()
    for i, coord in enumerate(deform_coords):
        shape_key.data[i].co = coord
    shape_key.value = 1
    return shape_key

def create_bevel_object():
    bpy.ops.mesh.primitive_plane_add()
    bpy.ops.object.convert(target="CURVE")
    bevel_obj = active_object()
    bevel_obj.scale.x = 0.26
    bevel_obj.scale.y = 0.05
    bevel_obj.name = "bevel_object"
    return bevel_obj

def animate_curve(shape_key, start_frame):
    start_value = 1
    mid_value = 0
    loop_length = 60
    shape_key.value = start_value
    shape_key.keyframe_insert("value", frame=start_frame)
    current_frame = start_frame + loop_length / 2
    shape_key.value = mid_value
    shape_key.keyframe_insert("value", frame=current_frame)
    current_frame = start_frame + loop_length
    shape_key.value = start_value
    shape_key.keyframe_insert("value", frame=current_frame)
    start_frame += 1
    return start_frame

def create_shape(vertices, radius, rotation, location):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=0.1)
    obj = active_object()
    obj.rotation_euler = rotation
    obj.location = location
    apply_random_color_material(obj)
    bpy.ops.object.modifier_add(type="BEVEL")
    obj.modifiers["Bevel"].width = 0.02
    return obj

def add_ctrl_empty(name=None):
    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()
    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"
    return empty_ctrl

def convert_srgb_to_linear_rgb(srgb_color_component):
    """
    Converting from sRGB to Linear RGB
    based on https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
    Video Tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    if srgb_color_component <= 0.04045:
        linear_color_component = srgb_color_component / 12.92
    else:
        linear_color_component = math.pow((srgb_color_component + 0.055) / 1.055, 2.4)
    return linear_color_component
class Axis:
    X = 0
    Y = 1
    Z = 2

def setup_scene(i=0):
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds
    project_name = "ring_loop"
    bpy.context.scene.render.image_settings.file_format = "FFMPEG"
    bpy.context.scene.render.ffmpeg.format = "MPEG4"
    bpy.context.scene.render.filepath = f"/tmp/project_{project_name}/loop_{i}.mp4"
    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()
    # Utility Building Blocks
    clean_scene()
    set_scene_props(fps, loop_seconds)
    loc = (20, -20, 12)
    rot = (math.radians(60), 0, math.radians(70))
    setup_camera(loc, rot)
    context = {
        "frame_count": frame_count,
    }
    return context

def animate_rotation(angle, axis_index, last_frame, obj=None, clockwise=False, linear=True, start_frame=1):
    if not obj:
        obj = active_object()
    frame = start_frame
    obj.keyframe_insert("rotation_euler", index=axis_index, frame=frame)
    if clockwise:
        angle_offset = -angle
    else:
        angle_offset = angle
    frame = last_frame
    obj.rotation_euler[axis_index] = math.radians(angle_offset) + obj.rotation_euler[axis_index]
    obj.keyframe_insert("rotation_euler", index=axis_index, frame=frame)
    if linear:
        set_fcurve_extrapolation_to_linear()

def set_scene_props(fps, loop_seconds):
    """
    Set scene properties
    """
    frame_count = fps * loop_seconds
    scene = bpy.context.scene
    scene.frame_end = frame_count
    # set the world background to black
    world = bpy.data.worlds["World"]
    if "Background" in world.node_tree.nodes:
        world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
    scene.render.fps = fps
    scene.frame_current = 1
    scene.frame_start = 1
    scene.render.engine = "CYCLES"
    # Use the GPU to render
    scene.cycles.device = "GPU"
    # Use the CPU to render
    # scene.cycles.device = "CPU"
    scene.cycles.samples = 300
    scene.view_settings.look = "Very High Contrast"
    set_1080p_render_res()

def remove_libraries():
    bpy.data.batch_remove(bpy.data.libraries)
@functools.cache

def get_script_path():
    # check if we are running from the Text Editor
    if bpy.context.space_data != None and bpy.context.space_data.type == "TEXT_EDITOR":
        print("bpy.context.space_data script_path")
        script_path = bpy.context.space_data.text.filepath
        if not script_path:
            print("ERROR: Can't get the script file folder path, because you haven't saved the script file.")
    else:
        print("__file__ script_path")
        script_path = __file__
    return script_path
@functools.cache

def add_lights():
    rig_obj, empty = create_light_rig(light_count=3, light_type="AREA", rig_radius=5.0, energy=150)
    rig_obj.location.z = 3
    bpy.ops.object.light_add(type="AREA", radius=5, location=(0, 0, 5))

def create_light_rig(light_count, light_type="AREA", rig_radius=2.0, light_radius=1.0, energy=100):
    bpy.ops.mesh.primitive_circle_add(vertices=light_count, radius=rig_radius)
    rig_obj = active_object()
    empty = add_ctrl_empty(name="empty.tracker-target.lights")
    for i in range(light_count):
        loc = rig_obj.data.vertices[i].co
        bpy.ops.object.light_add(type=light_type, radius=light_radius, location=loc)
        light = active_object()
        light.data.energy = energy
        light.parent = rig_obj
        bpy.ops.object.constraint_add(type="TRACK_TO")
        light.constraints["Track To"].target = empty
    return rig_obj, empty

def get_working_directory_path():
    """This function provides the folder path that the script will be operating from.
    There are examples of paths that you can use, just uncomment the path that you want to use.
    """
    # folder_path = pathlib.Path().home() / "tmp"
    folder_path = get_script_folder_path()
    # Examples of other folder paths
    ## Windows
    ### folder_path = pathlib.Path(r"E:\my_projects\project_123")
    ## Linux/macOS
    ### folder_path = pathlib.Path().home() / "my_projects" / "project_123"
    return folder_path
################################################################
# endregion helper functions END
################################################################

def get_list_of_blend_files(path):
    blend_files = []
    for blend_file_path in pathlib.Path(path).rglob("*.blend"):
        blend_files.append(blend_file_path)
    return blend_files

def create_floor_material():
    color = get_random_color()
    material = bpy.data.materials.new(name="floor_material")
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    if bpy.app.version < (4, 0, 0):
        material.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 0
    else:
        material.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0
    return material

def create_floor():
    path = get_working_directory_path() / "grid_floor.blend"
    if path.exists():
        link_objects(str(path))
    else:
        bpy.ops.mesh.primitive_plane_add(size=100)
        floor = active_object()
        material = bpy.data.materials.new(name="floor_material")
        material.diffuse_color = (0.0003, 0.0074, 0.0193, 1.0)
        floor.data.materials.append(material)

def prepare_scene(frame_count):
    create_floor()
    light_rig_obj, _ = create_light_rig(light_count=3)
    bpy.ops.object.empty_add()
    focus_empty = bpy.context.active_object
    animate_360_rotation(Axis.Z, frame_count)
    bpy.ops.object.camera_add()
    camera_obj = bpy.context.active_object
    bpy.context.scene.camera = camera_obj
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = focus_empty
    camera_obj.parent = focus_empty
    return camera_obj, focus_empty, light_rig_obj

def get_object_center(target_obj):
    bound_box_coord_sum = mathutils.Vector()
    for bound_box_coord in target_obj.bound_box:
        bound_box_coord_sum += mathutils.Vector(bound_box_coord)
    local_obj_center = bound_box_coord_sum / len(target_obj.bound_box)
    return target_obj.matrix_world @ local_obj_center

def focus_camera_on_target_obj(camera_obj, target_obj):
    make_active(target_obj)
    bpy.ops.view3d.camera_to_view_selected()
    # zoom out a bit to get some space between the edge of the camera and the object
    camera_obj.location *= 1.5

def update_scene(target_obj, focus_empty, camera_obj, light_rig_obj):
    obj_center = get_object_center(target_obj)
    focus_empty.location = obj_center
    height = target_obj.dimensions.z * 2
    camera_obj.location = (height, height, height)
    focus_camera_on_target_obj(camera_obj, target_obj)
    light_rig_obj.location.z = camera_obj.location.z

def run_turntable_render(model_name, output_folder_path):
    time_stamp = datetime.datetime.now().strftime("%H-%M-%S")
    scene = bpy.context.scene
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.filepath = str(output_folder_path / f"{model_name}_turntable_{time_stamp}.mp4")
    bpy.ops.render.render(animation=True)

def unlink_objects(objects):
    scene = bpy.context.scene
    # unlink objects from the
    for obj in objects:
        if obj is not None:
            scene.collection.objects.unlink(obj)

def get_random_color():
    return random.choice(
        [
            [0.92578125, 1, 0.0, 1],
            [0.203125, 0.19140625, 0.28125, 1],
            [0.8359375, 0.92578125, 0.08984375, 1],
            [0.16796875, 0.6796875, 0.3984375, 1],
            [0.6875, 0.71875, 0.703125, 1],
            [0.9609375, 0.9140625, 0.48046875, 1],
            [0.79296875, 0.8046875, 0.56640625, 1],
            [0.96484375, 0.8046875, 0.83984375, 1],
            [0.91015625, 0.359375, 0.125, 1],
            [0.984375, 0.4609375, 0.4140625, 1],
            [0.0625, 0.09375, 0.125, 1],
            [0.2578125, 0.9140625, 0.86328125, 1],
            [0.97265625, 0.21875, 0.1328125, 1],
            [0.87109375, 0.39453125, 0.53515625, 1],
            [0.8359375, 0.92578125, 0.08984375, 1],
            [0.37109375, 0.29296875, 0.54296875, 1],
            [0.984375, 0.4609375, 0.4140625, 1],
            [0.92578125, 0.16796875, 0.19921875, 1],
            [0.9375, 0.9609375, 0.96484375, 1],
            [0.3359375, 0.45703125, 0.4453125, 1],
        ]
    )

def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

def setup_camera(loc, rot):
    """
    create and setup the camera
    """
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    camera = active_object()
    # set the camera as the "active camera" in the scene
    bpy.context.scene.camera = camera
    # set the Focal Length of the camera
    camera.data.lens = 70
    camera.data.passepartout_alpha = 0.9
    empty = track_empty(camera)
    return empty

def setup_camera(loc, rot):
    """
    create and setup the camera
    """
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    camera = active_object()
    # set the camera as the "active camera" in the scene
    bpy.context.scene.camera = camera
    # set the Focal Length of the camera
    camera.data.lens = 70
    camera.data.passepartout_alpha = 0.9
    empty = track_empty(camera)
    return empty

def setup_scene(i=0):
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds
    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()
    project_name = "weave"
    render_folder = f"/tmp/project_{project_name}_{seed}/"
    render_pngs = True
    if render_pngs:
        bpy.context.scene.render.image_settings.file_format = "PNG"
        bpy.context.scene.render.filepath = render_folder
    else:
        bpy.context.scene.render.image_settings.file_format = "FFMPEG"
        bpy.context.scene.render.ffmpeg.format = "MPEG4"
        bpy.context.scene.render.filepath = f"{render_folder}/loop_{i}.mp4"
    # Utility Building Blocks
    clean_scene()
    set_scene_props(fps, loop_seconds)
    loc = (0, 0, 6)
    rot = (0, 0, 0)
    setup_camera(loc, rot)
    context = {
        "frame_count": frame_count,
    }
    return context

def enable_mod_tools():
    """
    enable Modifier Tools addon
    https://docs.blender.org/manual/en/3.0/addons/add_mesh/ant_landscape.html
    """
    enable_addon(addon_module_name="space_view3d_modifier_tools")

def get_random_color():
    return random.choice(
        [
            [0.92578125, 1, 0.0, 1],
            [0.203125, 0.19140625, 0.28125, 1],
            [0.8359375, 0.92578125, 0.08984375, 1],
            [0.16796875, 0.6796875, 0.3984375, 1],
            [0.6875, 0.71875, 0.703125, 1],
            [0.9609375, 0.9140625, 0.48046875, 1],
            [0.79296875, 0.8046875, 0.56640625, 1],
            [0.96484375, 0.8046875, 0.83984375, 1],
            [0.91015625, 0.359375, 0.125, 1],
            [0.984375, 0.4609375, 0.4140625, 1],
            [0.0625, 0.09375, 0.125, 1],
            [0.2578125, 0.9140625, 0.86328125, 1],
            [0.97265625, 0.21875, 0.1328125, 1],
            [0.87109375, 0.39453125, 0.53515625, 1],
            [0.8359375, 0.92578125, 0.08984375, 1],
            [0.37109375, 0.29296875, 0.54296875, 1],
            [0.984375, 0.4609375, 0.4140625, 1],
            [0.92578125, 0.16796875, 0.19921875, 1],
            [0.9375, 0.9609375, 0.96484375, 1],
            [0.3359375, 0.45703125, 0.4453125, 1],
        ]
    )

def enable_addon(addon_module_name):
    """
    Checkout this video explanation with example
    "How to enable add-ons with Python in Blender (with examples)"
    https://youtu.be/HnrInoBWT6Q
    """
    loaded_default, loaded_state = addon_utils.check(addon_module_name)
    if not loaded_state:
        addon_utils.enable(addon_module_name)

def enable_extra_curves():
    """
    Add Curve Extra Objects
    https://docs.blender.org/manual/en/latest/addons/add_curve/extra_objects.html
    """
    loaded_default, loaded_state = addon_utils.check("add_curve_extra_objects")
    if not loaded_state:
        addon_utils.enable("add_curve_extra_objects")

def create_emissive_material():
    color = get_random_color()
    material = bpy.data.materials.new(name="emissive_material")
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs["Emission"].default_value = color
    material.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 5.0
    return material

def add_lights():
    """
    I used this HDRI: https://polyhaven.com/a/dresden_station_night
    Please consider supporting polyhaven.com @ https://www.patreon.com/polyhaven/overview
    """
    # update the path to where you downloaded the HDRI
    path_to_image = r"C:\tmp\dresden_station_night_1k.exr"
    # Uncomment the next 2 lines for a Linux/macOS path to the HDRI in '~/tmp' folder
    # import os
    # path_to_image = f"{os.path.expanduser('~')}/tmp/dresden_station_night_1k.exr"
    color = (0, 0, 0, 0)
    apply_hdri(path_to_image, bg_color=color, hdri_light_strength=0.1, bg_strength=1)

def create_profile_curve():
    bpy.ops.curve.simple(
        Simple_Type='Arc', 
        Simple_endangle=180, 
        use_cyclic_u=False, 
        edit_mode=False)
    profile_curve = active_object()
    profile_curve.scale *= 0.1
    return profile_curve

def create_base_curve():
    bpy.ops.curve.spirals(
        spiral_type='TORUS', 
        turns=15, 
        steps=64, 
        cycles=1, 
        curves_number=4, 
        use_cyclic_u=True, 
        edit_mode=False)
    return active_object()

def animate_point_tilt(obj, frame_count):
    points = obj.data.splines.active.points
    
    for pnt in points:
        pnt.keyframe_insert("tilt", frame=1)
        pnt.tilt = math.radians(360)
        pnt.keyframe_insert("tilt", frame=frame_count + 1)
        
    make_spline_fcurve_interpolation_linear()

def create_primary_curve(profile_curve):
    primary_curve = create_base_curve()
    
    metal_material = create_metal_material()
    apply_material(metal_material)
    
    primary_curve.data.bevel_mode = 'OBJECT'
    primary_curve.data.bevel_object = profile_curve
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    return primary_curve

def setup_scene(i=0):
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds
    project_name = "stack_spin"
    bpy.context.scene.render.image_settings.file_format = "FFMPEG"
    bpy.context.scene.render.ffmpeg.format = "MPEG4"
    bpy.context.scene.render.filepath = f"/tmp/project_{project_name}/loop_{i}.mp4"
    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()
    # Utility Building Blocks
    clean_scene()
    set_scene_props(fps, loop_seconds)
    loc = (0, 0, 7)
    rot = (0, 0, 0)
    setup_camera(loc, rot, frame_count)
    context = {
        "frame_count": frame_count,
    }
    return context

def add_lights():
    bpy.ops.object.light_add(type="SUN")
    bpy.context.object.data.energy = 10

def create_circle_control_empty():
    empty = add_ctrl_empty(name=f"empty.circle.cntrl")
    empty.rotation_euler.z = math.radians(random.uniform(0, 360))
    empty.location.z = random.uniform(-3, 1)
    return empty

def clean_scene():
    """
    Removing all of the objects, collection, materials, particles,
    textures, images, curves, meshes, actions, nodes, and worlds from the scene
    Checkout this video explanation with example
    "How to clean the scene with Python in Blender (with examples)"
    https://youtu.be/3rNqVPtbhzc
    """
    # make sure the active object is not in Edit Mode
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()
    # make sure non of the objects are hidden from the viewport, selection, or disabled
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False
    # select all the object and delete them (just like pressing A + X + D in the viewport)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    # find all the collections and remove them
    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])
    # in the case when you modify the world shader
    # delete and recreate the world object
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]
    purge_orphans()

def time_seed():
    """
    Sets the random seed based on the time
    and copies the seed into the clipboard
    """
    seed = time.time()
    print(f"seed: {seed}")
    random.seed(seed)
    # add the seed value to your clipboard
    bpy.context.window_manager.clipboard = str(seed)
    return seed

def set_fcurve_interpolation_to_linear(obj=None):
    """loops over all the fcurve key frame points of an action
    and sets the interpolation to "LINEAR"
    """
    if obj is None:
        obj = active_object()
    for fcurve in bpy.context.active_object.animation_data.action.fcurves:
        for keyframe_point in fcurve.keyframe_points:
            keyframe_point.interpolation = "LINEAR"

def hex_color_to_rgb(hex_color):
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB
    Supports: "#RRGGBB" or "RRGGBB"
    Note: We are converting into Linear RGB since Blender uses a Linear Color Space internally
    https://docs.blender.org/manual/en/latest/render/color_management.html
    Video Tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    # remove the leading '#' symbol if present
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]
    assert len(hex_color) == 6, f"RRGGBB is the supported hex color format: {hex_color}"
    # extracting the Red color component - RRxxxx
    red = int(hex_color[:2], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_red = red / 255
    linear_red = convert_srgb_to_linear_rgb(srgb_red)
    # extracting the Green color component - xxGGxx
    green = int(hex_color[2:4], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_green = green / 255
    linear_green = convert_srgb_to_linear_rgb(srgb_green)
    # extracting the Blue color component - xxxxBB
    blue = int(hex_color[4:6], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_blue = blue / 255
    linear_blue = convert_srgb_to_linear_rgb(srgb_blue)
    return tuple([linear_red, linear_green, linear_blue])

def hex_color_str_to_rgba(hex_color: str):
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB with an Alpha of 1.0
    Supports: "#RRGGBB" or "RRGGBB"
    """
    # remove the leading '#' symbol if present
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]
    assert len(hex_color) == 6, "RRGGBB is the supported hex color format"
    # extracting the Red color component - RRxxxx
    red = int(hex_color[:2], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_red = red / 255
    linear_red = convert_srgb_to_linear_rgb(srgb_red)
    # extracting the Green color component - xxGGxx
    green = int(hex_color[2:4], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_green = green / 255
    linear_green = convert_srgb_to_linear_rgb(srgb_green)
    # extracting the Blue color component - xxxxBB
    blue = int(hex_color[4:6], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_blue = blue / 255
    linear_blue = convert_srgb_to_linear_rgb(srgb_blue)
    alpha = 1.0
    return tuple([linear_red, linear_green, linear_blue, alpha])

def create_data_animation_loop(obj, data_path, start_value, mid_value, start_frame, loop_length, linear_extrapolation=True):
    """
    To make a data property loop we need to:
    1. set the property to an initial value and add a keyframe in the beginning of the loop
    2. set the property to a middle value and add a keyframe in the middle of the loop
    3. set the property the initial value and add a keyframe at the end of the loop
    """
    # set the start value
    setattr(obj, data_path, start_value)
    # add a keyframe at the start
    obj.keyframe_insert(data_path, frame=start_frame)
    # set the middle value
    setattr(obj, data_path, mid_value)
    # add a keyframe in the middle
    mid_frame = start_frame + (loop_length) / 2
    obj.keyframe_insert(data_path, frame=mid_frame)
    # set the end value
    setattr(obj, data_path, start_value)
    # add a keyframe in the end
    end_frame = start_frame + loop_length
    obj.keyframe_insert(data_path, frame=end_frame)
    if linear_extrapolation:
        set_fcurve_extrapolation_to_linear()

def create_metal_material():
    color = get_random_color()
    material = bpy.data.materials.new(name="metal_material")
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    material.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
    return material

def scene_setup(i=0):
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds
    project_name = "stack_overflow"
    bpy.context.scene.render.image_settings.file_format = "FFMPEG"
    bpy.context.scene.render.ffmpeg.format = "MPEG4"
    bpy.context.scene.render.filepath = f"/tmp/project_{project_name}/loop_{i}.mp4"
    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()
    # Utility Building Blocks
    use_clean_scene_experimental = False
    if use_clean_scene_experimental:
        clean_scene_experimental()
    else:
        clean_scene()
    set_scene_props(fps, loop_seconds)
    z_coord = 1
    loc = (6.5, -3, z_coord)
    rot = (0, 0, 0)
    empty = setup_camera(loc, rot)
    empty.location.z = 2
    context = {
        "frame_count": frame_count,
        "frame_count_loop": frame_count + 1,
    }
    return context

def get_random_color():
    hex_color = random.choice(
        [
            "#FC766A",
            "#5B84B1",
            "#5F4B8B",
            "#E69A8D",
            "#42EADD",
            "#CDB599",
            "#00A4CC",
            "#F95700",
            "#00203F",
            "#ADEFD1",
            "#606060",
            "#D6ED17",
            "#ED2B33",
            "#D85A7F",
        ]
    )
    return hex_color_to_rgba(hex_color)

def create_bevel_obj():
    bpy.ops.curve.primitive_bezier_circle_add(radius=0.05, enter_editmode=False)
    return active_object()

def scene_setup(i=0):
    fps = 30
    loop_seconds = 6
    frame_count = fps * loop_seconds
    project_name = "hex_delay_spin"
    bpy.context.scene.render.image_settings.file_format = "FFMPEG"
    bpy.context.scene.render.ffmpeg.format = "MPEG4"
    bpy.context.scene.render.filepath = f"/tmp/project_{project_name}/loop_{i}.mp4"
    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()
    # Utility Building Blocks
    clean_scene()
    set_scene_props(fps, loop_seconds)
    loc = (0, 15, 0)
    rot = (0, 0, 0)
    setup_camera(loc, rot)
    context = {
        "frame_count": frame_count,
        "material": create_metallic_material(get_random_color()),
    }
    return context

def get_random_color():
    hex_color = random.choice(
        [
            "#846295",
            "#B369AC",
            "#BFB3CB",
            "#E3E0E7",
            "#F3F0E5",
            "#557E5F",
            "#739D87",
            "#C3CDB1",
            "#7F8BC3",
            "#0D2277",
            "#72ED72",
            "#40D4BC",
            "#7EADF0",
            "#EAEC71",
            "#C4C55D",
            "#EDE1D4",
            "#DBCBBD",
            "#A98E8E",
            "#676F84",
            "#4F5D6B",
            "#990065",
            "#C60083",
            "#FF00A9",
            "#F9D19C",
            "#BFB3A7",
            "#B3A598",
            "#998995",
            "#99A1A3",
            "#74817F",
            "#815D6D",
        ]
    )
    return hex_color_to_rgba(hex_color)

def animate_rotation(context, obj, i, frame_offset):
    start_frame = 10 + i * frame_offset
    obj.keyframe_insert("rotation_euler", frame=start_frame)
    # rotate mesh about the z-axis
    degrees = 180
    radians = math.radians(degrees)
    obj.rotation_euler.z = radians
    # rotate mesh about the y-axis
    degrees = 120
    radians = math.radians(degrees)
    obj.rotation_euler.y = radians
    end_frame = context["frame_count"] - 10
    obj.keyframe_insert("rotation_euler", frame=end_frame)
    make_fcurves_bounce()

def convert_srgb_to_linear_rgb(srgb_color_component):
    """
    Converting from sRGB to Linear RGB
    based on https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
    Video Tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    if srgb_color_component <= 0.04045:
        linear_color_component = srgb_color_component / 12.92
    else:
        linear_color_component = math.pow((srgb_color_component + 0.055) / 1.055, 2.4)
    return linear_color_component

def enable_import_images_as_planes():
    loaded_default, loaded_state = addon_utils.check("io_import_images_as_planes")
    if not loaded_state:
        addon_utils.enable("io_import_images_as_planes")

def add_light():
    bpy.ops.object.light_add(type="AREA", radius=6, location=(0, 0, 2))
    bpy.context.object.data.energy = 400
    bpy.context.object.data.color = hex_color_to_rgb("#F2E7DC")
    bpy.context.object.data.shape = "DISK"
    degrees = 180
    bpy.ops.object.light_add(type="AREA", radius=6, location=(0, 0, -2), rotation=(0.0, math.radians(degrees), 0.0))
    bpy.context.object.data.energy = 300
    bpy.context.object.data.color = hex_color_to_rgb("#F29F05")
    bpy.context.object.data.shape = "DISK"
@contextlib.contextmanager

def edit_mode():
    bpy.ops.object.mode_set(mode="EDIT")
    yield
    bpy.ops.object.mode_set(mode="OBJECT")

def create_data_animation_loop(obj, data_path, start_value, mid_value, start_frame, loop_length, linear_extrapolation=True):
    """
    To make a data property loop we need to:
    1. set the property to an initial value and add a keyframe in the beginning of the loop
    2. set the property to a middle value and add a keyframe in the middle of the loop
    3. set the property the initial value and add a keyframe at the end of the loop
    """
    # set the start value
    setattr(obj, data_path, start_value)
    # add a keyframe at the start
    obj.keyframe_insert(data_path, frame=start_frame)
    # set the middle value
    setattr(obj, data_path, mid_value)
    # add a keyframe in the middle
    mid_frame = start_frame + (loop_length) / 2
    obj.keyframe_insert(data_path, frame=mid_frame)
    # set the end value
    setattr(obj, data_path, start_value)
    # add a keyframe in the end
    end_frame = start_frame + loop_length
    obj.keyframe_insert(data_path, frame=end_frame)
    if linear_extrapolation:
        set_fcurve_extrapolation_to_linear()

def make_color_ramp_stops_from_colors(color_ramp_node, colors):
    """
    Use the provided colors to add apply them to the color ramp stops.
    Add new stops to the color ramp if needed.
    """
    color_count = len(colors)
    assert color_count > 1, "You need to provide at least two colors"
    # calculate the step between the color ramp stops
    step = 1 / color_count
    current_position = step
    # add new stops if necessary
    # we are subtracting 2 here because the color ramp comes with two stops
    for i in range(color_count - 2):
        color_ramp_node.elements.new(current_position)
        current_position += step
    # apply the colors to the stops
    for i, color in enumerate(colors):
        color_ramp_node.elements[i].color = color

def set_keyframe_point_interpolation_to_elastic(mesh_obj):
    for fcurve in mesh_obj.animation_data.action.fcurves:
        for keyframe_point in fcurve.keyframe_points:
            keyframe_point.interpolation = "ELASTIC"
            keyframe_point.easing = "AUTO"

def create_cast_to_sphere_animation_loop(context, mesh_obj):
    bpy.ops.object.modifier_add(type="CAST")
    create_data_animation_loop(
        mesh_obj.modifiers["Cast"],
        "factor",
        start_value=0.01,
        mid_value=1,
        start_frame=1,
        loop_length=context["frame_count"],
        linear_extrapolation=False
    )
    
    set_keyframe_point_interpolation_to_elastic(mesh_obj)

def create_mesh_instance(context):
    bpy.ops.mesh.primitive_cube_add(size=0.18)
    mesh_instance = active_object()
    mesh_instance.name = "mesh_instance"
    subdivide(number_cuts=5)
    bpy.ops.object.shade_smooth()
    create_cast_to_sphere_animation_loop(context, mesh_instance)
    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].segments = 16
    bpy.context.object.modifiers["Bevel"].width = 0.01
    material, nodes = create_base_material()
    mesh_instance.data.materials.append(material)
    colors = context["colors"]
    make_color_ramp_stops_from_colors(nodes["ColorRamp"].color_ramp, colors)
    return mesh_instance

def create_centerpiece(context):
    mesh_instance = create_mesh_instance(context)
    primary_mesh = create_primary_mesh(context)
    mesh_instance.parent = primary_mesh

def animate_rotation(angle, axis_index, last_frame, obj=None, clockwise=False, linear=True, start_frame=1):
    if not obj:
        obj = active_object()
    frame = start_frame
    obj.keyframe_insert("rotation_euler", index=axis_index, frame=frame)
    if clockwise:
        angle_offset = -angle
    else:
        angle_offset = angle
    frame = last_frame
    obj.rotation_euler[axis_index] = math.radians(angle_offset) + obj.rotation_euler[axis_index]
    obj.keyframe_insert("rotation_euler", index=axis_index, frame=frame)
    if linear:
        set_fcurve_extrapolation_to_linear()

def apply_rotation():
    bpy.ops.object.transform_apply(rotation=True)

def apply_random_rotation():
    obj = active_object()
    obj.rotation_euler.x = math.radians(random.uniform(0, 360))
    obj.rotation_euler.y = math.radians(random.uniform(0, 360))
    obj.rotation_euler.z = math.radians(random.uniform(0, 360))
    apply_rotation()

def apply_emission_material(color, name=None, energy=1):
    material = create_emission_material(color, name=name, energy=energy)
    obj = active_object()
    obj.data.materials.append(material)

def rotate_object(axis, degrees):
    bpy.context.active_object.rotation_euler[axis] = math.radians(degrees)

def create_reflective_material(color, name=None, roughness=0.1, specular=0.5, return_nodes=False):
    if name is None:
        name = ""
    material = bpy.data.materials.new(name=f"material.reflective.{name}")
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    material.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = roughness
    material.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = specular
    if return_nodes:
        return material, material.node_tree.nodes
    else:
        return material

def add_light():
    bpy.ops.object.light_add(type="AREA", radius=1, location=(0, 0, 2))
    bpy.context.object.data.energy = 100
    bpy.context.object.data.color = get_random_color()[:3]
    bpy.context.object.data.shape = "DISK"

def apply_glare_composite_effect():
    bpy.context.scene.use_nodes = True
    render_layer_node = bpy.context.scene.node_tree.nodes.get("Render Layers")
    comp_node = bpy.context.scene.node_tree.nodes.get("Composite")
    # remove node_glare from the previous run
    old_node_glare = bpy.context.scene.node_tree.nodes.get("Glare")
    if old_node_glare:
        bpy.context.scene.node_tree.nodes.remove(old_node_glare)
    # create Glare node
    node_glare = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeGlare")
    node_glare.size = 7
    node_glare.glare_type = "FOG_GLOW"
    node_glare.quality = "HIGH"
    node_glare.threshold = 0.2
    # create links
    bpy.context.scene.node_tree.links.new(render_layer_node.outputs["Image"], node_glare.inputs["Image"])
    bpy.context.scene.node_tree.links.new(node_glare.outputs["Image"], comp_node.inputs["Image"])

def apply_metaball_material():
    color = get_random_color()
    material = create_reflective_material(color, name="metaball", roughness=0.1, specular=0.5)
    primary_metaball = bpy.data.metaballs[0]
    primary_metaball.materials.append(material)

def create_metaball_path(context):
    bpy.ops.curve.primitive_bezier_circle_add()
    path = active_object()
    path.data.path_duration = context["frame_count"]
    animate_360_rotation(Axis.X, context["frame_count"], path, clockwise=random.randint(0, 1))
    apply_random_rotation()
    if random.randint(0, 1):
        path.scale.x *= random.uniform(0.1, 0.4)
    else:
        path.scale.y *= random.uniform(0.1, 0.4)
    return path

def create_centerpiece(context, color):
    frame_step = 6
    buffer = 1
    count = int((context["frame_count_loop"] * 2) / frame_step) + buffer
    current_frame = -context["frame_count_loop"]
    surface = make_surface(color)
    for _ in range(count):
        duplicate_surface = duplicate_object(surface)
        animate_object_update(context, duplicate_surface, current_frame)
        current_frame += frame_step

def create_background():
    create_floor()
    create_emissive_ring()

def create_emissive_ring():
    # add a circle mesh into the scene
    bpy.ops.mesh.primitive_circle_add(vertices=128, radius=5.5)
    # get a reference to the currently active object
    ring_obj = bpy.context.active_object
    ring_obj.name = "ring.emissive"
    # rotate ring by 90 degrees
    ring_obj.rotation_euler.x = math.radians(90)
    # convert mesh into a curve
    bpy.ops.object.convert(target="CURVE")
    # add bevel to curve
    ring_obj.data.bevel_depth = 0.05
    ring_obj.data.bevel_resolution = 16
    # create and assign an emissive material
    ring_material = create_emissive_ring_material()
    ring_obj.data.materials.append(ring_material)

def create_emissive_ring_material():
    color = get_random_color()
    material = bpy.data.materials.new(name="emissive_ring_material")
    material.use_nodes = True
    if bpy.app.version < (4, 0, 0):
        material.node_tree.nodes["Principled BSDF"].inputs["Emission"].default_value = color
    else:
        material.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = color
    material.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 30.0
    return material

def create_metal_ring_material():
    color = get_random_color()
    material = bpy.data.materials.new(name="metal_ring_material")
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    material.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
    return material

def animate_rotation(context, ring_obj, z_rotation, y_rotation):
    # rotate mesh about the y-axis
    degrees = y_rotation
    radians = math.radians(degrees)
    ring_obj.rotation_euler.y = radians
    # rotate mesh about the z-axis
    degrees = z_rotation
    radians = math.radians(degrees)
    ring_obj.rotation_euler.z = radians
    # insert keyframe at frame one
    start_frame = 1
    ring_obj.keyframe_insert("rotation_euler", frame=start_frame)
    # rotate mesh about the y-axis
    degrees = y_rotation + 360
    radians = math.radians(degrees)
    ring_obj.rotation_euler.y = radians
    # rotate mesh about the z-axis
    degrees = z_rotation + 360 * 2
    radians = math.radians(degrees)
    ring_obj.rotation_euler.z = radians
    # insert keyframe after the last frame (to make a seamless loop)
    end_frame = context["frame_count"] + 1
    ring_obj.keyframe_insert("rotation_euler", frame=end_frame)
    # make keyframe interpolation linear
    make_fcurves_linear()

def setup_camera(loc, rot):
    """
    create and setup the camera
    """
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    camera = active_object()
    # set the camera as the "active camera" in the scene
    bpy.context.scene.camera = camera
    # set the Focal Length of the camera
    camera.data.lens = 45
    camera.data.passepartout_alpha = 0.9
    empty = track_empty(camera)

def render_loop():
    bpy.ops.render.render(animation=True)

def gen_centerpiece(context):
    for _ in range(3):
        bpy.ops.mesh.primitive_cube_add(size=random.uniform(1, 3))
        cube = active_object()
        bpy.ops.object.modifier_add(type="WIREFRAME")
        cube.modifiers["Wireframe"].thickness = random.uniform(0.03, 0.1)
        animate_object_rotation(context, cube)
        apply_material(cube)

def setup_scene():
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds
    project_name = "loop_grid"
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.filepath = f"/tmp/project_{project_name}/"
    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()
    # Utility Building Blocks
    clean_scene()
    set_scene_props(fps, loop_seconds)
    loc = (0, 0, 5)
    rot = (0, 0, 0)
    setup_camera(loc, rot)

def add_light():
    bpy.ops.object.light_add(type="SUN")
    sun = active_object()
    sun.data.energy = 2
    sun.data.specular_factor = 0
    sun.data.use_shadow = False

def get_list_of_loops():
    return [
        "c:\\tmp\\project_cube_loops\\loop_0.mp4",
        "c:\\tmp\\project_cube_loops\\loop_1.mp4",
        "c:\\tmp\\project_cube_loops\\loop_10.mp4",
        "c:\\tmp\\project_cube_loops\\loop_11.mp4",
        "c:\\tmp\\project_cube_loops\\loop_12.mp4",
        "c:\\tmp\\project_cube_loops\\loop_13.mp4",
        "c:\\tmp\\project_cube_loops\\loop_14.mp4",
        "c:\\tmp\\project_cube_loops\\loop_15.mp4",
        "c:\\tmp\\project_cube_loops\\loop_2.mp4",
        "c:\\tmp\\project_cube_loops\\loop_3.mp4",
        "c:\\tmp\\project_cube_loops\\loop_4.mp4",
        "c:\\tmp\\project_cube_loops\\loop_5.mp4",
        "c:\\tmp\\project_cube_loops\\loop_6.mp4",
        "c:\\tmp\\project_cube_loops\\loop_7.mp4",
        "c:\\tmp\\project_cube_loops\\loop_8.mp4",
        "c:\\tmp\\project_cube_loops\\loop_9.mp4",
    ]

def clean_sequencer(sequence_context):
    bpy.ops.sequencer.select_all(sequence_context, action="SELECT")
    bpy.ops.sequencer.delete(sequence_context)

def remove_compositor_nodes():
    bpy.context.scene.node_tree.nodes.clear()

def get_image_files(image_folder_path, image_extention=".png"):
    image_files = list()
    for file_name in os.listdir(image_folder_path):
        if file_name.endswith(image_extention):
            image_files.append(file_name)
    image_files.sort()
    pprint.pprint(image_files)
    return image_files

def find_sequence_editor():
    for area in bpy.context.window.screen.areas:
        if area.type == "SEQUENCE_EDITOR":
            return area
    return None

def set_up_output_params(image_folder_path, image_files, fps):
    frame_count = len(image_files)
    scene = bpy.context.scene
    scene.frame_end = frame_count
    image_path = os.path.join(image_folder_path, image_files[0])
    width, height = get_image_dimensions(image_path)
    scene.render.resolution_y = height
    scene.render.resolution_x = width
    scene.render.fps = fps
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.constant_rate_factor = "PERC_LOSSLESS"
    now = datetime.now()
    time = now.strftime("%H-%M-%S")
    filepath = os.path.join(image_folder_path, f"anim_{time}.mp4")
    scene.render.filepath = filepath

def render_loop():
    bpy.ops.render.render(animation=True)

def add_lights():
    rotation = (math.radians(60), 0.0, math.radians(180))
    bpy.ops.object.light_add(type="SUN", rotation=rotation)
    bpy.context.object.data.energy = 100
    bpy.context.object.data.diffuse_factor = 0.05
    bpy.context.object.data.angle = math.radians(45)

def loop_param(obj, param_name, start_value, mid_value, frame_count):
    frame = 1
    setattr(obj, param_name, start_value)
    obj.keyframe_insert(param_name, frame=frame)
    frame = frame_count / 2
    setattr(obj, param_name, mid_value)
    obj.keyframe_insert(param_name, frame=frame)
    frame = frame_count
    setattr(obj, param_name, start_value)
    obj.keyframe_insert(param_name, frame=frame)

def set_keyframe_to_ease_in_out(obj):
    for fcurve in obj.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = "BACK"
            kf.easing = "EASE_IN_OUT"

def animate_shape(obj, vertices, start_frame, end_frame):
    obj.keyframe_insert("rotation_euler", frame=start_frame)
    one_turn = 360 / vertices
    obj.rotation_euler.z += math.radians(one_turn * 2)
    obj.keyframe_insert("rotation_euler", frame=end_frame)
    set_keyframe_to_ease_in_out(obj)

def set_up_output_params(folder_path):
    scene = bpy.context.scene
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.constant_rate_factor = "PERC_LOSSLESS"
    now = datetime.datetime.now()
    time = now.strftime("%H-%M-%S")
    filepath = os.path.join(folder_path, f"stitched_together_{time}.mp4")
    scene.render.filepath = filepath

def clean_proxies(video_folder_path):
    """
    This will delete the BL_proxies folder
    """
    
    def on_error(function, path, excinfo):
        print(f"Failed to remove {path}\n{excinfo}")
    bl_proxy_path = os.path.join(video_folder_path, "BL_proxy")
    if os.path.exists(bl_proxy_path):
        print(f"Removing the BL_proxies folder in {bl_proxy_path}")
        shutil.rmtree(bl_proxy_path, ignore_errors=False, onerror=on_error)

def trim_the_video(clip_start_offset_frame, clip_frame_count):
    # trim the start of the clip
    bpy.context.active_sequence_strip.frame_offset_start = clip_start_offset_frame
    # trim the end of the clip
    bpy.context.active_sequence_strip.frame_final_duration = clip_frame_count

def move_the_clip_into_position(start_frame_pos, clip_start_offset_frame):
    bpy.context.active_sequence_strip.frame_start = start_frame_pos - clip_start_offset_frame

def apply_fade_in_to_clip(clip_transition_overlap):
    # make sure the clips overlap
    bpy.context.active_sequence_strip.frame_start -= clip_transition_overlap
    bpy.ops.sequencer.fades_add(type="IN")

def convert_srgb_to_linear_rgb(srgb_color_component):
    """
    Converting from sRGB to Linear RGB
    based on https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
    Video Tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    if srgb_color_component <= 0.04045:
        linear_color_component = srgb_color_component / 12.92
    else:
        linear_color_component = math.pow((srgb_color_component + 0.055) / 1.055, 2.4)
    return linear_color_component

def duplicate_object(obj=None, linked=False):
    """
    Duplicate object
    Args:
        obj: source object that will be duplicated.
        linked: link duplicated object to target source.
    """
    if obj is None:
        obj = active_object()
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.duplicate(linked=linked)
    duplicate_obj = active_object()
    return duplicate_obj

def enable_extra_curves():
    """
    enable Add Curve Extra Objects addon
    https://docs.blender.org/manual/en/3.0/addons/add_curve/extra_objects.html
    """
    enable_addon(addon_module_name="add_curve_extra_objects")

def convert_srgb_to_linear_rgb(srgb_color_component):
    """
    Converting from sRGB to Linear RGB
    based on https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
    Video Tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    if srgb_color_component <= 0.04045:
        linear_color_component = srgb_color_component / 12.92
    else:
        linear_color_component = math.pow((srgb_color_component + 0.055) / 1.055, 2.4)
    return linear_color_component

def deselect_all_objects():
    """
    Similar to bpy.ops.object.select_all(action="DESELECT")
    """
    for obj in bpy.data.objects:
        obj.select_set(False)

def create_collection(collection_name):
    deselect_all_objects()
    collection = bpy.data.collections.new(name=collection_name)
    bpy.context.scene.collection.children.link(collection)
    return collection

def add_to_collection(collection_name, obj=None, base_collection=None):
    """
    Adds a given object to a collection with collection_name
    """
    if obj is None:
        obj = active_object()
    if base_collection is None:
        base_collection = bpy.context.scene.collection
    collection = bpy.data.collections.get(collection_name)
    if collection is None:
        logging.error("couldn't find a collection with the name '%s' ", collection_name)
        return
    collection.objects.link(obj)
    base_collection.objects.unlink(obj)

def make_instance_of_collection(collection_name, location, rotation_euler=None, base_collection=None):
    source_collection = bpy.data.collections.get(collection_name)
    if source_collection is None:
        logging.error("couldn't find a collection with the name '%s' ", collection_name)
        return
    if base_collection is None:
        base_collection = bpy.context.scene.collection
    new_name = f"{collection_name}.instance.{str(location)}"
    collection_instance = bpy.data.objects.new(name=new_name, object_data=None)
    collection_instance.location = location
    collection_instance.instance_type = "COLLECTION"
    collection_instance.instance_collection = source_collection
    base_collection.objects.link(collection_instance)
    if rotation_euler:
        collection_instance.rotation_euler = rotation_euler
    return collection_instance
class Axis:
    X = 0
    Y = 1
    Z = 2

def apply_reflective_material(color, name=None, roughness=0.1, specular=0.5):
    material = create_reflective_material(color, name=name, roughness=roughness, specular=specular)
    obj = active_object()
    obj.data.materials.append(material)

def set_up_world_sun_light(sun_config=None, strength=1.0):
    world_node_tree = bpy.context.scene.world.node_tree
    world_node_tree.nodes.clear()
    node_location_x_step = 300
    node_location_x = 0
    node_sky = world_node_tree.nodes.new(type="ShaderNodeTexSky")
    node_location_x += node_location_x_step
    world_background_node = world_node_tree.nodes.new(type="ShaderNodeBackground")
    world_background_node.inputs["Strength"].default_value = strength
    world_background_node.location.x = node_location_x
    node_location_x += node_location_x_step
    world_output_node = world_node_tree.nodes.new(type="ShaderNodeOutputWorld")
    world_output_node.location.x = node_location_x
    if sun_config:
        logging.info("Updating ShaderNodeTexSky params:")
        for attr, value in sun_config.items():
            if hasattr(node_sky, attr):
                logging.info("\t %s set to %s", attr, str(value))
                setattr(node_sky, attr, value)
            else:
                logging.warning("\t %s is not an attribute of ShaderNodeTexSky node", attr)
    world_node_tree.links.new(node_sky.outputs["Color"], world_background_node.inputs["Color"])
    world_node_tree.links.new(world_background_node.outputs["Background"], world_output_node.inputs["Surface"])
    return node_sky
# bpybb end

def convert_srgb_to_linear_rgb(srgb_color_component):
    """
    Converting from sRGB to Linear RGB
    based on https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
    """
    if srgb_color_component <= 0.04045:
        linear_color_component = srgb_color_component / 12.92
    else:
        linear_color_component = math.pow((srgb_color_component + 0.055) / 1.055, 2.4)
    return linear_color_component

def load_color_palettes():
    """
    download the json file with the palettes from
    https://github.com/CGArtPython/get-color-palettes-py/blob/main/palettes/100_five_color_palettes.json
    """
    # create path to json file with color palettes
    # on Windows this path should resolve to C:/tmp/100_five_color_palettes.json
    path = os.path.abspath("/tmp/100_five_color_palettes.json")
    if os.name != 'nt':
        # when running on macOS or Linux
        # this path should resolve to ~/tmp/100_five_color_palettes.json
        user_folder = os.path.expanduser("~")
        path = user_folder + path
    # load the color palettes
    with open(path, "r") as color_palettes_file:
        color_palettes = json.loads(color_palettes_file.read())
    return color_palettes

def get_random_color():
    color_palette = get_color_palette()
    hex_color = random.choice(color_palette)
    return hex_color_to_rgba(hex_color)

def scene_setup(i=0):
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds
    project_name = "truchet_201"
    bpy.context.scene.render.image_settings.file_format = "FFMPEG"
    bpy.context.scene.render.ffmpeg.format = "MPEG4"
    bpy.context.scene.render.filepath = f"/tmp/project_{project_name}/loop_{i}.mp4"
    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()
    # Utility Building Blocks
    use_clean_scene_experimental = False
    if use_clean_scene_experimental:
        clean_scene_experimental()
    else:
        clean_scene()
    set_scene_props(fps, loop_seconds)
    context = {
        "frame_count": frame_count,
        "frame_count_loop": frame_count + 1,
    }
    return context

def animate_truchet_tile(context, truchet_tile):
    frame_step = context["frame_count"] / 4
    frame = 1
    truchet_tile.keyframe_insert("rotation_euler", index=Axis.Z, frame=frame)
    truchet_tile.rotation_euler.z += math.radians(90)
    frame += frame_step
    truchet_tile.keyframe_insert("rotation_euler", index=Axis.Z, frame=frame)
    frame += frame_step
    truchet_tile.keyframe_insert("rotation_euler", index=Axis.Z, frame=frame)
    truchet_tile.rotation_euler.z += math.radians(90)
    frame += frame_step
    truchet_tile.keyframe_insert("rotation_euler", index=Axis.Z, frame=frame)

def create_truchet_tile_pattern(context, truchet_tile_size, collection_name):
    # Note: we need to enable the "Add Curve Extra Objects" addon
    tile_pattern_size = truchet_tile_size / 2
    bpy.ops.curve.simple(
        location=(-tile_pattern_size, -tile_pattern_size, 0),
        Simple_Type="Arc",
        Simple_endangle=90,
        Simple_radius=tile_pattern_size,
        use_cyclic_u=False,
        edit_mode=False,
    )
    tile_part_1 = active_object()
    tile_part_1.data.extrude = 0.15
    bpy.ops.object.modifier_add(type="SOLIDIFY")
    tile_part_1.modifiers["Solidify"].thickness = 0.1
    tile_part_1.modifiers["Solidify"].offset = 0
    bpy.ops.object.convert(target="MESH")
    bpy.ops.object.shade_smooth()
    bpy.ops.object.shade_smooth(use_auto_smooth=True)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
    tile_part_2 = duplicate_object()
    rotate_object(Axis.Z, 180)
    join_objects([tile_part_1, tile_part_2])
    add_to_collection(collection_name)
    apply_reflective_material(context["first_color"], roughness=0.5)
    tile = active_object()
    tile.name = "tile_pattern"
    return tile

def create_truchet_tile(context, truchet_tile_size, collection_name):
    truchet_tile = create_truchet_tile_pattern(context, truchet_tile_size, collection_name)
    animate_truchet_tile(context, truchet_tile)
    return truchet_tile

def create_truchet_tile_platform(context, truchet_tile_size):
    collection_name = "truchet_tile_platform"
    create_collection(collection_name=collection_name)
    ctrl_empty = add_ctrl_empty()
    ctrl_empty.name = "platform_ctrl"
    add_to_collection(collection_name)
    bpy.ops.mesh.primitive_plane_add(size=truchet_tile_size)
    add_to_collection(collection_name)
    plane = active_object()
    plane.parent = ctrl_empty
    apply_reflective_material(context["second_color"], roughness=1.0)
    truchet_tile = create_truchet_tile(context, truchet_tile_size, collection_name)
    truchet_tile.parent = ctrl_empty
    return collection_name

def create_truchet_tile_platform_group(step_x, step_y, x_range, y_range, base_truchet_tile_collection):
    current_x = step_x
    start_y = step_y
    platform_group_collection_name = "truchet_tiles_group"
    create_collection(collection_name=platform_group_collection_name)
    for _ in range(x_range):
        current_y = start_y
        for _ in range(y_range):
            loc = (current_x, current_y, 0)
            new_collection_obj = make_instance_of_collection(base_truchet_tile_collection, loc)
            make_active(new_collection_obj)
            add_to_collection(platform_group_collection_name)
            current_deg_rot = random.choice([0, 90])
            new_collection_obj.rotation_euler.z = math.radians(current_deg_rot)
            current_y += step_y
        current_x += step_x
    return platform_group_collection_name

def animate_camera(context, section_step, camera_ctrl_empty):
    frame = 1
    camera_ctrl_empty.keyframe_insert("location", index=Axis.X, frame=frame)
    camera_ctrl_empty.location.x += section_step * 2
    camera_ctrl_empty.keyframe_insert("location", index=Axis.X, frame=context["frame_count_loop"])
    make_active(camera_ctrl_empty)
    set_fcurve_extrapolation_to_linear()

def setup_scene(i=0):
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds
    project_name = "color_palettes"
    bpy.context.scene.render.image_settings.file_format = "FFMPEG"
    bpy.context.scene.render.ffmpeg.format = "MPEG4"
    bpy.context.scene.render.filepath = f"/tmp/project_{project_name}/loop_{i}.mp4"
    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()
    # Utility Building Blocks
    clean_scene()
    set_scene_props(fps, loop_seconds)
    loc = (0, 0, 15)
    rot = (0, 0, 0)
    setup_camera(loc, rot)
    context = {
        "frame_count": frame_count,
    }
    return context

def convert_srgb_to_linear_rgb(srgb_color_component):
    """
    Converting from sRGB to Linear RGB
    based on https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
    Args:
    - srgb_color_component (float): The sRGB color component value
    Returns:
    - linear_color_component (float): The linear RGB color component value
    """
    if srgb_color_component <= 0.04045:
        linear_color_component = srgb_color_component / 12.92
    else:
        linear_color_component = math.pow((srgb_color_component + 0.055) / 1.055, 2.4)
    return linear_color_component

def setup_scene(palette_index, seed=0):
    """
    Sets up the scene for rendering with the specified palette index and seed.
    Args:
    - palette_index (int): The index of the color palette to use.
    - seed (float, optional): The random seed to use. If not provided, a new seed will be generated based on the current time.
    """
    if seed:
        random.seed(seed)
    else:
        seed = time_seed()
    project_name = "applying_1k_color_palettes"
    render_dir_path = pathlib.Path.home() / project_name / f"palette_{palette_index}_seed_{seed}.png"
    render_dir_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.filepath = str(render_dir_path)

def prepare_and_render_scene(palette, palette_index, seed=None):
    """
    Prepares and renders the scene with the specified palette and index.
    Args:
    - palette (list): The color palette to use for updating the colors.
    - palette_index (int): The index of the color palette.
    - seed (float, optional): The random seed to use. If not provided, a new seed will be generated based on the current time.
    """
    setup_scene(palette_index, seed)
    update_colors(palette)
    bpy.ops.render.render(write_still=True)

def render_all_palettes(palettes):
    """
    Renders all the color palettes.
    Args:
        palettes (list): A list of color palettes to be rendered.
    """
    # make sure we are using the EEVEE render engine for faster rendering
    bpy.context.scene.render.engine = "BLENDER_EEVEE"
    start_time = time.time()
    for palette_index, palette in enumerate(palettes):
        prepare_and_render_scene(palette, palette_index)
        # remove the following line to render all the palettes
        break
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

def set_1080px_square_render_res():
    """
    Set the resolution of the rendered image to 1080 by 1080
    """
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080

def enable_addon(addon_module_name):
    """
    Checkout this video explanation with example
    "How to enable add-ons with Python in Blender (with examples)"
    https://youtu.be/HnrInoBWT6Q
    """
    loaded_default, loaded_state = addon_utils.check(addon_module_name)
    if not loaded_state:
        addon_utils.enable(addon_module_name)

def enable_extra_meshes():
    """
    enable Add Mesh Extra Objects addon
    https://docs.blender.org/manual/en/3.0/addons/add_mesh/mesh_extra_objects.html
    """
    enable_addon(addon_module_name="add_mesh_extra_objects")

def create_metallic_material(color, name=None, roughness=0.1, return_nodes=False):
    if name is None:
        name = ""
    material = bpy.data.materials.new(name=f"material.metallic.{name}")
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    material.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = roughness
    material.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
    if return_nodes:
        return material, material.node_tree.nodes
    else:
        return material

def create_light_rig(light_count, light_type="AREA", rig_radius=2.0, light_radius=1.0, energy=100):
    bpy.ops.mesh.primitive_circle_add(vertices=light_count, radius=rig_radius)
    rig_obj = active_object()
    empty = add_empty(name=f"empty.tracker-target.lights")
    for i in range(light_count):
        loc = rig_obj.data.vertices[i].co
        bpy.ops.object.light_add(type=light_type, radius=light_radius, location=loc)
        light = active_object()
        light.data.energy = energy
        light.parent = rig_obj
        bpy.ops.object.constraint_add(type="TRACK_TO")
        light.constraints["Track To"].target = empty
    return rig_obj, empty

def make_surface(color):
    # this operator is found in the "Add Mesh Extra Objects" add-on
    bpy.ops.mesh.primitive_z_function_surface(div_x=64, div_y=64, size_x=1, size_y=1)
    surface = active_object()
    bpy.ops.object.shade_smooth()
    surface.data.use_auto_smooth = True
    bpy.ops.object.modifier_add(type="SOLIDIFY")
    bpy.ops.object.modifier_add(type="BEVEL")
    surface.modifiers["Bevel"].width = 0.001
    surface.modifiers["Bevel"].limit_method = "NONE"
    # this operator is found in the "Modifier Tools" add-on
    bpy.ops.object.apply_all_modifiers()
    apply_metallic_material(color, name="metallic", roughness=random.uniform(0.35, 0.65))
    return surface

def update_object(obj):
    obj.scale *= 1.5
    obj.location.z = 2
    obj.rotation_euler.z = math.radians(270)

def select_random_color_palette(context):
    return random.choice(context["color_palettes"])

def create_color_plane(hex_color):
    # add a plane into the scene and scale it down
    bpy.ops.mesh.primitive_plane_add()
    plane = active_object()
    plane.scale.y *= 0.2
    # create a material and apply the provided hex color to the base color
    material = bpy.data.materials.new(name=f"hex_color_{hex_color}")
    material.diffuse_color = hex_color_str_to_rgba(hex_color)
    # add material to object
    plane.data.materials.append(material)
    return plane

def create_text_object(text):
    bpy.ops.object.text_add()
    text_obj = active_object()
    text_obj.scale *= 0.3
    text_obj.data.body = text
    bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS", center="MEDIAN")
    text_obj.location = 0, 0, 0
    text_obj.data.extrude = 0.07
    text_obj.data.fill_mode = "NONE"
    text_obj.data.bevel_depth = 0.02
    return text_obj

def get_image_files(image_folder_path, image_extension=".png"):
    image_files = list()
    for file_name in os.listdir(image_folder_path):
        if file_name.endswith(image_extension):
            image_files.append(file_name)
    image_files.sort()
    pprint.pprint(image_files)
    return image_files

def add_compositor_nodes(image_sequence, duration):
    """
    Find the Compositor Nodes we need here
    https://docs.blender.org/api/current/bpy.types.CompositorNode.html#bpy.types.CompositorNode
    """
    scene = bpy.context.scene
    compositor_node_tree = scene.node_tree
    image_node = compositor_node_tree.nodes.new(type="CompositorNodeImage")
    image_node.image = image_sequence
    image_node.frame_duration = duration
    composite_node = compositor_node_tree.nodes.new(type="CompositorNodeComposite")
    composite_node.location.x = 200
    viewer_node = compositor_node_tree.nodes.new(type="CompositorNodeViewer")
    viewer_node.location.x = 200
    viewer_node.location.y = -200
    # create links
    compositor_node_tree.links.new(image_node.outputs["Image"], composite_node.inputs["Image"])
    compositor_node_tree.links.new(image_node.outputs["Image"], viewer_node.inputs["Image"])



