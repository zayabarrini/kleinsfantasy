"""
See YouTube tutorial here:
"""
import functools
import logging
import math
import pprint
import random
import time

import addon_utils
import bpy

################################################################
# helper functions BEGIN
################################################################


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


def clean_scene_experimental():
    """
    This might crash Blender!
    Proceed at your own risk!
    But it will clean the scene.
    """
    old_scene_name = "to_delete"
    bpy.context.window.scene.name = old_scene_name
    bpy.ops.scene.new()
    bpy.data.scenes.remove(bpy.data.scenes[old_scene_name])

    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


def active_object():
    """
    returns the currently active object
    """
    return bpy.context.active_object


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


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def duplicate_object(obj=None, linked=False):
    if obj is None:
        obj = active_object()

    deselect_all_objects()

    obj.select_set(True)

    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.duplicate(linked=linked)
    dup_obj = active_object()

    return dup_obj


def make_active(obj):
    deselect_all_objects()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

    return empty


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
    enable Add Curve Extra Objects addon
    https://docs.blender.org/manual/en/3.0/addons/add_curve/extra_objects.html
    """
    enable_addon(addon_module_name="add_curve_extra_objects")


def join_objects(objects):
    deselect_all_objects()

    for obj in objects:
        obj.select_set(True)

    bpy.ops.object.join()

    new_obj = active_object()

    return new_obj


def set_1080px_square_render_res():
    """
    Set the resolution of the rendered image to 1080 by 1080
    """
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080


def set_fcurve_extrapolation_to_linear():
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


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


def hex_color_to_rgba(hex_color, alpha=1.0):
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB with an Alpha passed as a parameter

    Supports: "#RRGGBB" or "RRGGBB"

    Video Tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    linear_red, linear_green, linear_blue = hex_color_to_rgb(hex_color)
    return tuple([linear_red, linear_green, linear_blue, alpha])


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


def configure_logging(level=logging.INFO):
    logging.basicConfig(level=level)


@functools.cache
def load_color_palettes():
    return [
        ["#69D2E7", "#A7DBD8", "#E0E4CC", "#F38630", "#FA6900"],
        ["#FE4365", "#FC9D9A", "#F9CDAD", "#C8C8A9", "#83AF9B"],
        ["#ECD078", "#D95B43", "#C02942", "#542437", "#53777A"],
        ["#556270", "#4ECDC4", "#C7F464", "#FF6B6B", "#C44D58"],
        ["#1B325F", "#9CC4E4", "#E9F2F9", "#3A89C9", "#F26C4F"],
        ["#E8DDCB", "#CDB380", "#036564", "#033649", "#031634"],
        ["#490A3D", "#BD1550", "#E97F02", "#F8CA00", "#8A9B0F"],
        ["#594F4F", "#547980", "#45ADA8", "#9DE0AD", "#E5FCC2"],
        ["#00A0B0", "#6A4A3C", "#CC333F", "#EB6841", "#EDC951"],
        ["#413D3D", "#040004", "#C8FF00", "#FA023C", "#4B000F"],
        ["#3FB8AF", "#7FC7AF", "#DAD8A7", "#FF9E9D", "#FF3D7F"],
        ["#CCF390", "#E0E05A", "#F7C41F", "#FC930A", "#FF003D"],
        ["#395A4F", "#432330", "#853C43", "#F25C5E", "#FFA566"],
        ["#343838", "#005F6B", "#008C9E", "#00B4CC", "#00DFFC"],
        ["#AAFF00", "#FFAA00", "#FF00AA", "#AA00FF", "#00AAFF"],
        ["#00A8C6", "#40C0CB", "#F9F2E7", "#AEE239", "#8FBE00"],
    ]


def select_random_color_palette():
    random_palette = random.choice(load_color_palettes())
    print("Random palette:")
    pprint.pprint(random_palette)
    return random_palette


@functools.cache
def get_color_palette():
    """Note: we will select a random color palette once.
    With the functools.cache decorator we will return the same palette.
    """
    return select_random_color_palette()


def get_random_color():
    color_palette = get_color_palette()
    hex_color = random.choice(color_palette)
    return hex_color_to_rgba(hex_color)


def select_color_pair():
    first_color = get_random_color()
    second_color = get_random_color()
    while second_color == first_color:
        second_color = get_random_color()
    return first_color, second_color


def setup_camera():
    """
    create and setup the camera
    """
    bpy.ops.object.camera_add()
    camera = active_object()

    # set the camera as the "active camera" in the scene
    bpy.context.scene.camera = camera

    # set the Focal Length of the camera
    camera.data.lens = 70

    camera.data.passepartout_alpha = 0.9

    empty = track_empty(camera)
    camera.parent = empty

    return camera, empty


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


################################################################
# helper functions END
################################################################


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


def create_and_animate_camera(context, section_step):
    camera, camera_ctrl_empty = setup_camera()

    camera_ctrl_empty.location = (section_step, (section_step / 3), 0)

    camera.location.x += section_step / 2
    camera.location.y = -section_step / 2 + section_step / 10
    camera.location.z = section_step / 2

    animate_camera(context, section_step, camera_ctrl_empty)


def create_centerpiece(context):

    truchet_tile_size = 2
    base_truchet_tile_collection = create_truchet_tile_platform(context, truchet_tile_size)

    step_x = truchet_tile_size
    step_y = truchet_tile_size
    x_range = 12
    y_range = 12
    platform_group_collection_name = create_truchet_tile_platform_group(step_x, step_y, x_range, y_range, base_truchet_tile_collection)

    section_instance_count = 3
    section_step = step_x * x_range
    for i in range(1, section_instance_count + 1):
        loc = (section_step * i, 0, 0)
        make_instance_of_collection(platform_group_collection_name, loc)

    create_and_animate_camera(context, section_step)


def main():
    """
    Python code to generate this animation
    https://www.artstation.com/artwork/g2lDPx
    """
    configure_logging()

    enable_extra_curves()

    context = scene_setup()
    context["first_color"], context["second_color"] = select_color_pair()

    create_centerpiece(context)

    sun_config = {"sun_rotation": math.radians(random.uniform(0, 360))}
    set_up_world_sun_light(sun_config, strength=0.1)


if __name__ == "__main__":
    main()

"""
This script is used to render color palettes in Blender. It loads color palettes from a JSON file, selects a random color palette, and updates the colors of materials and nodes in the Blender scene based on the selected palette. The scene is then rendered and saved as a PNG image.

The script contains several helper functions for tasks such as setting the random seed, converting hex color strings to RGBA values, selecting random color palettes, choosing random colors from a palette, and updating colors in the scene.

To use the script, simply run it. By default, it will render all the color palettes loaded from the JSON file. You can also specify a specific color palette index and random seed to render a single palette.

Note: This script assumes that the JSON file containing the color palettes is located at the path specified in the `load_color_palettes` function.
"""

import json
import math
import pathlib
import random
import time

import bpy

################################################################
# helper functions BEGIN
################################################################


def time_seed():
    """
    Sets the random seed based on the time
    and copies the seed into the clipboard

    Returns:
    - seed (int): The random seed based on the current time.
    """
    seed = int(time.time())
    print(f"seed: {seed}")
    random.seed(seed)

    # add the seed value to your clipboard
    bpy.context.window_manager.clipboard = str(seed)

    return seed


def hex_color_str_to_rgba(hex_color: str):
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB with an Alpha of 1.0

    Args:
    - hex_color (str): The hex color string in the format "#RRGGBB" or "RRGGBB"

    Returns:
    - rgba_color (tuple): The Linear RGB color with an Alpha of 1.0
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


def choose_random_color(palette, exclude_colors=None):
    """
    Chooses a random color from the given palette, excluding the specified colors if provided.

    Args:
    - palette (list): The color palette to choose from.
    - exclude_colors (list, optional): The colors to exclude from the selection.

    Returns:
    - color (str): The randomly selected color.
    """
    if not exclude_colors:
        return random.choice(palette)

    while True:
        color = random.choice(palette)
        if color not in exclude_colors:
            return color


################################################################
# helper functions END
################################################################


def load_color_palettes():
    """
    Loads the color palettes from a JSON file.

    Returns:
    - color_palettes (list): The list of color palettes loaded from the JSON file.
    """
    # https://github.com/CGArtPython/get_color_palettes_py/blob/main/palettes/1000_five_color_palettes.json
    path = pathlib.Path.home() / "tmp" / "1000_five_color_palettes.json"
    with open(path, "r") as color_palette:
        color_palettes = json.loads(color_palette.read())

    return color_palettes


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


def update_colors(palette):
    """
    Updates the colors of the materials and nodes in the Blender scene based on the given palette.

    Args:
    - palette (list): The color palette to use for updating the colors.
    """
    random.shuffle(palette)

    palette = [hex_color_str_to_rgba(hex_color) for hex_color in palette]

    backdrop_bsdf_node = bpy.data.materials["backdrop"].node_tree.nodes["Principled BSDF"]
    backdrop_color = choose_random_color(palette)
    backdrop_bsdf_node.inputs["Base Color"].default_value = backdrop_color

    upper_platform_bsdf_node = bpy.data.materials["upper_platform"].node_tree.nodes["Principled BSDF"]
    platform_color = choose_random_color(palette, exclude_colors=[backdrop_color])
    upper_platform_bsdf_node.inputs["Base Color"].default_value = platform_color

    pillar_bsdf_node = bpy.data.materials["pillar"].node_tree.nodes["Principled BSDF"]
    pillar_color = choose_random_color(palette, exclude_colors=[backdrop_color, platform_color])
    pillar_bsdf_node.inputs["Base Color"].default_value = pillar_color

    icing_bsdf_node = bpy.data.materials["icing"].node_tree.nodes["Principled BSDF"]
    icing_color = choose_random_color(palette, exclude_colors=[backdrop_color])
    icing_bsdf_node.inputs["Base Color"].default_value = pillar_color

    color_ramp = bpy.data.materials["sprinkles"].node_tree.nodes["ColorRamp"].color_ramp
    color_ramp.elements[0].color = choose_random_color(palette, exclude_colors=[icing_color])
    color_ramp.elements[1].color = choose_random_color(palette, exclude_colors=[icing_color])
    color_ramp.elements[2].color = choose_random_color(palette, exclude_colors=[icing_color])
    color_ramp.elements[3].color = choose_random_color(palette, exclude_colors=[icing_color])


def main():
    """
    The main entry point of the script.
    """
    palettes = load_color_palettes()

    palette_index = None
    seed = None

    if palette_index is not None and seed is not None:
        bpy.context.scene.render.engine = "CYCLES"
        selected_palette = palettes[palette_index]
        prepare_and_render_scene(selected_palette, palette_index, seed)
        return

    render_all_palettes(palettes)


if __name__ == "__main__":
    main()
"""
See YouTube tutorial here: https://www.youtube.com/watch?v=BSsjSj0iOaE
"""
import datetime
import functools
import math
import pathlib

import bpy
import mathutils

################################################################
# region helper functions BEGIN
################################################################


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
    returns the currently active object
    """
    return bpy.context.active_object


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = f"empty.{name}"
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def set_fcurve_extrapolation_to_linear(obj=None):
    """
    Loops over all the fcurves of an action
    and sets the extrapolation to "LINEAR".
    """
    if obj is None:
        obj = active_object()

    for fcurve in obj.animation_data.action.fcurves:
        fcurve.extrapolation = "LINEAR"


class Axis:
    X = 0
    Y = 1
    Z = 2


def animate_360_rotation(axis_index, last_frame, obj=None, clockwise=False, linear=True, start_frame=1):
    animate_rotation(360, axis_index, last_frame, obj, clockwise, linear, start_frame)


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


def set_1080p_render_res():
    """
    Set the resolution of the rendered image to 1080p
    """
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080


# bpybb end


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
def get_script_folder_path():
    script_path = get_script_path()
    return pathlib.Path(script_path).resolve().parent


def scene_setup():
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds

    clean_scene()
    remove_libraries()

    for lib in bpy.data.libraries:
        bpy.data.batch_remove(ids=(lib,))

    set_scene_props(fps, loop_seconds)

    context = {
        "frame_count": frame_count,
        "loop_frame_count": frame_count + 1,
    }

    return context


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


def link_objects(blend_file_path, with_name=None):

    # link the blender file objects into the current blender file
    with bpy.data.libraries.load(blend_file_path, link=True) as (data_from, data_to):
        data_to.objects = data_from.objects

    scene = bpy.context.scene

    linked_objects = []

    # link the objects into the scene collection
    for obj in data_to.objects:
        if obj is None:
            continue

        if with_name and with_name not in obj.name:
            continue

        scene.collection.objects.link(obj)
        linked_objects.append(obj)

    return linked_objects


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


def render_turntable_models(context, blend_files):

    camera_obj, focus_empty, light_rig_obj = prepare_scene(context["loop_frame_count"])

    # we will be looking for models with this text in their name
    target_substr_name = "target"
    for blend_file in blend_files:
        print(f"processing {blend_file}")
        objects = link_objects(str(blend_file), with_name=target_substr_name)

        if not objects:
            print(f"didn't find any model with '{target_substr_name}' in it's name in {blend_file}")
            continue

        target_obj = objects[0]

        update_scene(target_obj, focus_empty, camera_obj, light_rig_obj)

        print(f"rendering turntable {blend_file}")
        output_folder_path = pathlib.Path(blend_file).parent
        run_turntable_render(target_obj.name, output_folder_path)

        unlink_objects(objects)


def main():
    """
    A script that finds all blend files under a path,
    links the target models into the current scene, and renders a turntable loop .mp4
    """
    context = scene_setup()

    # example of a path in your home folder
    models_folder_path = get_working_directory_path() / "models"

    blend_files = get_list_of_blend_files(models_folder_path)

    render_turntable_models(context, blend_files)


if __name__ == "__main__":
    main()
"""
Note: set_up_world_sun_light() is avalible via the bpybb Python package.
https://github.com/CGArtPython/bpy_building_blocks
"""

import math
import random

import bpy


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
        print("Updating ShaderNodeTexSky params:")
        for attr, value in sun_config.items():
            if hasattr(node_sky, attr):
                print("\t %s set to %s", attr, str(value))
                setattr(node_sky, attr, value)
            else:
                print("\t warning: %s is not an attribute of ShaderNodeTexSky node", attr)

    world_node_tree.links.new(node_sky.outputs["Color"], world_background_node.inputs["Color"])
    world_node_tree.links.new(world_background_node.outputs["Background"], world_output_node.inputs["Surface"])


def main():
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))

    bpy.ops.mesh.primitive_plane_add(size=100)
    plane_obj = bpy.context.active_object
    material = bpy.data.materials.new(name="my_material")
    plane_obj.data.materials.append(material)
    material.diffuse_color = (0.1, 0.1, 0.1, 1.0)

    sun_config = {"sun_rotation": math.radians(random.randint(0, 360))}

    set_up_world_sun_light(sun_config=sun_config, strength=0.2)


if __name__ == "__main__":
    main()
# extend Python's functionality to work with time and dates
import datetime
# extend Python's functionality to work with JSON files
import json
# extend Python's math functionality
import math
# extend Python's functionality to work with file paths
import pathlib

# give Python access to Blender's functionality
import bpy

__rig_obj_tag__ = "brainstorm"

################################################################
# region helper functions BEGIN
################################################################


def get_output_folder_path():
    return pathlib.Path.home() / "tmp"


def get_metadata_folder_path():
    output_path = get_output_folder_path()
    metadata_folder_path = output_path / "metadata"
    if not metadata_folder_path.exists():
        metadata_folder_path.mkdir()
    return metadata_folder_path


def parent(child_obj, parent_obj, keep_transform=False):
    """Parent the child object to the parent object"""
    child_obj.parent = parent_obj
    if keep_transform:
        child_obj.matrix_parent_inverse = parent_obj.matrix_world.inverted()


def create_empty():
    bpy.ops.object.empty_add()
    empty_obj = bpy.context.active_object

    empty_obj.name = f"empty.{__rig_obj_tag__}"

    starting_empty_loc = (0.0, 0.0, 0.1)
    empty_obj.location = starting_empty_loc
    return empty_obj


def create_camera(empty_obj):
    bpy.ops.object.camera_add()
    camera_obj = bpy.context.active_object

    camera_obj.name = f"camera.{__rig_obj_tag__}"

    starting_cam_loc = (1.2, -1.4, 0.9)
    camera_obj.location = starting_cam_loc
    parent(camera_obj, empty_obj, keep_transform=True)

    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty_obj

    return camera_obj


def create_area_light(empty_obj):
    bpy.ops.object.light_add(type="AREA")
    area_light_obj = bpy.context.active_object

    area_light_obj.name = f"area_light.{__rig_obj_tag__}"

    starting_light_loc = (-10.5, 9.0, 3)
    area_light_obj.location = starting_light_loc
    starting_light_rot = (0.2, -1.15, -1.0)
    area_light_obj.rotation_euler = starting_light_rot

    parent(area_light_obj, empty_obj, keep_transform=True)

    return area_light_obj


def create_rig():
    empty_obj = create_empty()

    camera_obj = create_camera(empty_obj)

    area_light_obj = create_area_light(empty_obj)

    return empty_obj, camera_obj, area_light_obj


def remove_rig():
    """Remove any rig objects that were left from the previous run"""
    objects_to_remove = [obj for obj in bpy.data.objects if __rig_obj_tag__ in obj.name]

    for obj in objects_to_remove:
        bpy.data.objects.remove(obj)


def scene_setup(full_resolution=False):
    remove_rig()

    empty_obj, camera_obj, area_light_obj = create_rig()

    bpy.context.scene.camera = camera_obj

    if full_resolution:
        bpy.context.scene.cycles.samples = 300
        bpy.context.scene.render.resolution_percentage = 100
    else:
        bpy.context.scene.cycles.samples = 50
        bpy.context.scene.render.resolution_percentage = 50

    return empty_obj, camera_obj, area_light_obj


################################################################
# endregion helper functions END
################################################################


def get_scene_configurations():
    return [
        {
            "light_power": 1000,
            "light_location": (-10.5, 9.0, 3),
            "light_rotation": (math.radians(10), math.radians(-65), math.radians(-60)),
            "light_scale": (1.0, 1.0, 1.0),
            "camera_focal_length": 40,
        },
        {
            "light_power": 2500,
            "light_location": (-10.5, 9.0, 3),
            "light_rotation": (math.radians(10), math.radians(-65), math.radians(-20)),
            "light_scale": (1.0, 2.0, 1.0),
            "camera_focal_length": 50,
        },
        {
            "light_power": 1500,
            "light_location": (-10.5, 9.0, 3),
            "light_rotation": (math.radians(10), math.radians(-65), math.radians(-20)),
            "light_scale": (1.4, 1.0, 1.0),
            "camera_focal_length": 60,
        },
    ]


def apply_scene_configuration(scene_config, empty_obj, camera_obj, area_light_obj):
    empty_obj.rotation_euler.z = math.radians(scene_config["empty_z_rotation"])

    area_light_obj.location = scene_config["light_location"]
    area_light_obj.rotation_euler = scene_config["light_rotation"]
    area_light_obj.scale = scene_config["light_scale"]
    area_light_obj.data.energy = scene_config["light_power"]

    camera_obj.location.z = scene_config["camera_z_loc"]
    camera_obj.data.lens = scene_config["camera_focal_length"]


def render_scene():

    output_folder_path = get_output_folder_path()
    time_stamp = datetime.datetime.now().strftime("%H-%M-%S")
    image_name = f"{__rig_obj_tag__}_{time_stamp}"
    bpy.context.scene.render.filepath = str(output_folder_path / f"{image_name}.png")

    bpy.ops.render.render(write_still=True)

    return image_name


def save_scene_configuration(image_name, scene_config):
    """Save the scene configuration into a json file and place it into the metadata folder"""
    metadata_folder_path = get_metadata_folder_path()
    metadata_file_name = str(metadata_folder_path / f"{image_name}.json")
    with open(metadata_file_name, "w") as metadata_file_obj:
        text = json.dumps(scene_config, indent=4)
        metadata_file_obj.write(text)


def extract_scene_configuration(image_name):
    """Based on the image name find the metadata for that image"""
    metadata_folder_path = get_metadata_folder_path()
    metadata_file_name = metadata_folder_path / f"{image_name}.json"

    if metadata_file_name.exists():
        with open(str(metadata_file_name), "r") as metadata_file_obj:
            text = metadata_file_obj.read()
            data = json.loads(text)
        return data
    else:
        print(f"ERROR: {metadata_file_name} scene configuration does not exist")

    return None


def load_scene_configuration(image_name):
    """Based on the image name find the metadata and apply it"""
    empty_obj, camera_obj, area_light_obj = scene_setup(full_resolution=True)

    scene_configuration = extract_scene_configuration(image_name)

    if scene_configuration:
        apply_scene_configuration(scene_configuration, empty_obj, camera_obj, area_light_obj)


def render_scene_configurations():

    empty_obj, camera_obj, area_light_obj = scene_setup()

    scene_configurations = get_scene_configurations()

    empty_z_rotation_step = 30
    current_empty_z_rotation = 0

    camera_z_loc_start = 0.9
    camera_z_loc_step = 0.1
    camera_z_loc_step_count = 3

    while current_empty_z_rotation < 360:

        current_camera_z_loc = camera_z_loc_start

        for _ in range(camera_z_loc_step_count):
            for scene_config in scene_configurations:
                scene_config["empty_z_rotation"] = current_empty_z_rotation
                scene_config["camera_z_loc"] = current_camera_z_loc

                apply_scene_configuration(scene_config, empty_obj, camera_obj, area_light_obj)

                image_name = render_scene()

                save_scene_configuration(image_name, scene_config)

            current_camera_z_loc -= camera_z_loc_step

        current_empty_z_rotation += empty_z_rotation_step


def main():
    """
    Brainstorming Reverse Key Lighting scene setup.

    Inspired by Gleb Alexandrov's tutorial
    One Simple Technique to Improve Your Lighting in Blender | Reverse Key Lighting
    https://www.youtube.com/watch?v=jrCtpmdAhF0
    """
    # If you like one of the created images you can set load_scene_config to True and
    # set image_name to the image name
    load_scene_config = False

    if load_scene_config:
        image_name = "brainstorm_15-34-16"
        load_scene_configuration(image_name)
    else:
        render_scene_configurations()


if __name__ == "__main__":
    main()
import os
import pathlib
import pprint

import bpy


def remove_compositor_nodes():
    bpy.context.scene.node_tree.nodes.clear()


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


def import_image_sequence_into_compositor(image_folder_path, fps):
    image_files = get_image_files(image_folder_path)

    file_info = list()
    for image_name in image_files:
        file_info.append({"name": image_name})

    bpy.ops.image.open(directory=image_folder_path, files=file_info)

    scene = bpy.context.scene
    scene.use_nodes = True

    remove_compositor_nodes()

    image_data_name = image_files[0]
    image_sequence = bpy.data.images[image_data_name]
    duration = len(image_files)
    add_compositor_nodes(image_sequence, duration)

    scene.frame_end = duration
    width, height = image_sequence.size
    scene.render.resolution_y = height
    scene.render.resolution_x = width
    scene.render.fps = fps


def main():
    """
    Python code to import a folder with png(s) into the compositor as a sequence of images.
    """
    image_folder_path = str(pathlib.Path.home() / "tmp" / "my_project")
    fps = 30
    import_image_sequence_into_compositor(image_folder_path, fps)


if __name__ == "__main__":
    main()
import math
import random
import time

import bpy

################################################################
# helper functions BEGIN
################################################################


def purge_orphans():
    """
    Remove all orphan data blocks

    see this from more info:
    https://youtu.be/3rNqVPtbhzc?t=149
    """
    if bpy.app.version >= (3, 0, 0):
        # run this only for Blender versions 3.0 and higher
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True, do_linked_ids=True, do_recursive=True
        )
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


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

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


def set_1k_square_render_res():
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
        world.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)

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

    set_1k_square_render_res()


def setup_scene(i=0):
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds

    project_name = "cube_loops"
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


def make_fcurves_linear():
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


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


def apply_material(obj):
    color = get_random_color()
    mat = bpy.data.materials.new(name="Material")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    mat.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 0

    obj.data.materials.append(mat)


def add_lights():
    rot = (math.radians(60), 0, math.radians(120))

    bpy.ops.object.light_add(type="SUN", rotation=rot)
    bpy.context.object.data.energy = 10
    bpy.context.object.data.angle = math.radians(180)
    bpy.context.object.data.use_shadow = False


def render_loop():
    bpy.ops.render.render(animation=True)


################################################################
# helper functions END
################################################################


def animate_object_rotation(context, obj):

    frame = 1
    obj.rotation_euler.x = math.radians(random.uniform(-360, 360))
    obj.keyframe_insert("rotation_euler", index=0, frame=frame)
    obj.rotation_euler.y = math.radians(random.uniform(-360, 360))
    obj.keyframe_insert("rotation_euler", index=1, frame=frame)
    obj.rotation_euler.z = math.radians(random.uniform(-360, 360))
    obj.keyframe_insert("rotation_euler", index=2, frame=frame)

    frame += context["frame_count"]

    rotations = [-3, -2, -1, 0, 1, 2, 3]
    obj.rotation_euler.x += math.radians(360) * random.choice(rotations)
    obj.keyframe_insert("rotation_euler", index=0, frame=frame)
    obj.rotation_euler.y += math.radians(360) * random.choice(rotations)
    obj.keyframe_insert("rotation_euler", index=1, frame=frame)
    obj.rotation_euler.z += math.radians(360) * random.choice(rotations)
    obj.keyframe_insert("rotation_euler", index=2, frame=frame)

    make_fcurves_linear()


def gen_centerpiece(context):
    for _ in range(3):

        bpy.ops.mesh.primitive_cube_add(size=random.uniform(1, 3))
        cube = active_object()

        bpy.ops.object.modifier_add(type="WIREFRAME")
        cube.modifiers["Wireframe"].thickness = random.uniform(0.03, 0.1)

        animate_object_rotation(context, cube)
        apply_material(cube)


def gen_background():
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -5))
    obj = active_object()
    apply_material(obj)


def main():
    """
    Python code to generate simple loop animations with cubes

    Tutorial: https://www.youtube.com/watch?v=GgX7rGcrHVI
    """
    count = 16
    for i in range(count):
        context = setup_scene(i)
        add_lights()
        gen_centerpiece(context)
        gen_background()
        # render_loop()


if __name__ == "__main__":
    main()
"""
Python code to generate this animation
https://www.artstation.com/artwork/0nVn4V

Based on a phyllotaxis pattern created by formula 4.1 from
http://algorithmicbotany.org/papers/abop/abop-ch4.pdf

Inspired by Dan Shiffman's Coding Challenge #30: Phyllotaxis
https://www.youtube.com/watch?v=KWoJgHFYWxY&t=0s

"""

import math
import random
import time

import bpy

################################################################
# helper functions BEGIN
################################################################


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
    returns the currently active object
    """
    return bpy.context.active_object


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


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

    return empty


def set_1080px_square_render_res():
    """
    Set the resolution of the rendered image to 1080 by 1080
    """
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080


def set_fcurve_extrapolation_to_linear():
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


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


def hex_color_to_rgba(hex_color, alpha=1.0):
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB with an Alpha passed as a parameter

    Supports: "#RRGGBB" or "RRGGBB"

    Video Tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    linear_red, linear_green, linear_blue = hex_color_to_rgb(hex_color)
    return tuple([linear_red, linear_green, linear_blue, alpha])


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


def create_emission_material(color, name=None, energy=30, return_nodes=False):
    if name is None:
        name = ""

    material = bpy.data.materials.new(name=f"material.emission.{name}")
    material.use_nodes = True

    out_node = material.node_tree.nodes.get("Material Output")
    bsdf_node = material.node_tree.nodes.get("Principled BSDF")
    material.node_tree.nodes.remove(bsdf_node)

    node_emission = material.node_tree.nodes.new(type="ShaderNodeEmission")
    node_emission.inputs["Color"].default_value = color
    node_emission.inputs["Strength"].default_value = energy

    node_emission.location = 0, 0

    material.node_tree.links.new(node_emission.outputs["Emission"], out_node.inputs["Surface"])

    if return_nodes:
        return material, material.node_tree.nodes
    else:
        return material


def render_loop():
    bpy.ops.render.render(animation=True)


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

    bpy.context.object.data.dof.use_dof = True
    bpy.context.object.data.dof.aperture_fstop = 0.1

    return empty


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
        world.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)

    scene.render.fps = fps

    scene.frame_current = 1
    scene.frame_start = 1

    bpy.context.scene.eevee.use_bloom = True

    scene.view_settings.look = "Very High Contrast"

    set_1080px_square_render_res()


def scene_setup(i=0):
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds

    project_name = "floret"
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

    loc = (0, 0, 80)
    rot = (0, 0, 0)
    setup_camera(loc, rot)

    context = {
        "frame_count": frame_count,
        "fps": fps,
    }

    return context


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


################################################################
# helper functions END
################################################################


def calculate_end_frame(context, current_frame):
    # make sure the end frame is divisible by the FPS
    quotient, remainder = divmod(current_frame, context["fps"])

    if remainder != 0:
        bpy.context.scene.frame_end = (quotient + 1) * context["fps"]
    else:
        bpy.context.scene.frame_end = current_frame

    return bpy.context.scene.frame_end


def animate_depth_of_field(frame_end):

    start_focus_distance = 15.0
    mid_focus_distance = bpy.data.objects["Camera"].location.z / 2
    start_frame = 1
    loop_length = frame_end
    create_data_animation_loop(
        bpy.data.objects["Camera"].data.dof,
        "focus_distance",
        start_focus_distance,
        mid_focus_distance,
        start_frame,
        loop_length,
        linear_extrapolation=False,
    )


def calculate_phyllotaxis_coordinates(n, angle, scale_fac):
    """
    calculating a point in a phyllotaxis pattern based on formula 4.1 from
    http://algorithmicbotany.org/papers/abop/abop-ch4.pdf

    See tutorial for detailed description: https://youtu.be/aeDbYuJyXr8
    """
    # calculate "φ" in formula (4.1) http://algorithmicbotany.org/papers/abop/abop-ch4.pdf
    current_angle = n * angle

    # calculate "r" in formula (4.1) http://algorithmicbotany.org/papers/abop/abop-ch4.pdf
    current_radius = scale_fac * math.sqrt(n)

    # convert from Polar Coordinates (r,φ) to Cartesian Coordinates (x,y)
    x = current_radius * math.cos(current_angle)
    y = current_radius * math.sin(current_angle)

    return x, y


def create_centerpiece(context):

    colors = (hex_color_to_rgba("#306998"), hex_color_to_rgba("#FFD43B"))

    ico_sphere_radius = 0.2

    # "c" in formula (4.1) http://algorithmicbotany.org/papers/abop/abop-ch4.pdf
    scale_fac = 1.0

    # "α" angle in radians in formula (4.1) http://algorithmicbotany.org/papers/abop/abop-ch4.pdf
    angle = math.radians(random.uniform(137.0, 138.0))

    # set angle to the Fibonacci angle 137.5 to get the sunflower pattern
    # angle = math.radians(137.5)

    current_frame = 1
    frame_step = 0.5
    start_emission_strength_value = 0
    mid_emission_strength_value = 20
    loop_length = 60

    count = 300
    for n in range(count):

        x, y = calculate_phyllotaxis_coordinates(n, angle, scale_fac)

        # place ico sphere
        bpy.ops.mesh.primitive_ico_sphere_add(radius=ico_sphere_radius, location=(x, y, 0))
        obj = active_object()

        # assign an emission material
        material, nodes = create_emission_material(color=random.choice(colors), name=f"{n}_sphr", energy=30, return_nodes=True)
        obj.data.materials.append(material)

        # animate the Strength value of the emission material
        create_data_animation_loop(
            nodes["Emission"].inputs["Strength"],
            "default_value",
            start_emission_strength_value,
            mid_emission_strength_value,
            current_frame,
            loop_length,
            linear_extrapolation=False,
        )

        current_frame += frame_step

    current_frame = int(current_frame + loop_length)
    end_frame = calculate_end_frame(context, current_frame)

    animate_depth_of_field(end_frame)


def main():
    """
    Python code to generate this animation
    https://www.artstation.com/artwork/0nVn4V
    """
    context = scene_setup()
    create_centerpiece(context)


if __name__ == "__main__":
    main()
import math
import random
import time

import bpy

################################################################
# helper functions BEGIN
################################################################


def purge_orphans():
    """
    Remove all orphan data blocks

    see this from more info:
    https://youtu.be/3rNqVPtbhzc?t=149
    """
    if bpy.app.version >= (3, 0, 0):
        # run this only for Blender versions 3.0 and higher
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True, do_linked_ids=True, do_recursive=True
        )
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


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add()
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

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

    camera.data.dof.use_dof = True
    camera.data.dof.focus_object = empty
    camera.data.dof.aperture_fstop = 0.1

    return empty


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

    scene.eevee.use_bloom = True
    scene.eevee.bloom_intensity = 0.005

    # set Ambient Occlusion properties
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 4
    scene.eevee.gtao_factor = 5

    scene.eevee.taa_render_samples = 64

    scene.view_settings.look = "Very High Contrast"
    bpy.context.preferences.edit.use_negative_frames = True

    set_1080px_square_render_res()


def setup_scene(i=0):
    fps = 30
    loop_seconds = 6
    frame_count = fps * loop_seconds

    project_name = "outgoing_circles"
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
    setup_camera(loc, rot)

    context = {
        "frame_count": frame_count,
    }

    return context


def make_fcurves_linear():
    for fcurve in bpy.context.active_object.animation_data.action.fcurves:
        for points in fcurve.keyframe_points:
            points.interpolation = "LINEAR"


def get_random_color():
    return random.choice(
        [
            [0.48046875, 0.171875, 0.5, 0.99609375],
            [0.3515625, 0.13671875, 0.39453125, 0.99609375],
            [0.2734375, 0.21484375, 0.08984375, 0.99609375],
            [0.5625, 0.45703125, 0.234375, 0.99609375],
            [0.92578125, 0.8828125, 0.77734375, 0.99609375],
            [0.1640625, 0.4921875, 0.13671875, 0.99609375],
            [0.453125, 0.74609375, 0.328125, 0.99609375],
            [0.2734375, 0.21484375, 0.08984375, 0.99609375],
            [0.5625, 0.45703125, 0.234375, 0.99609375],
            [0.92578125, 0.8828125, 0.77734375, 0.99609375],
            [0.1640625, 0.4921875, 0.13671875, 0.99609375],
            [0.453125, 0.74609375, 0.328125, 0.99609375],
            [0.00390625, 0.11328125, 0.15625, 0.99609375],
            [0.0234375, 0.49609375, 0.46875, 0.99609375],
            [0.01953125, 0.51953125, 0.6953125, 0.99609375],
            [0, 0.66796875, 0.78515625, 0.99609375],
            [0, 0.15234375, 0.171875, 0.99609375],
            [0.3203125, 0, 0.12890625, 0.99609375],
            [0.56640625, 0, 0.2265625, 0.99609375],
            [0.99609375, 0, 0.3984375, 0.99609375],
            [0.9453125, 0.640625, 0.33203125, 0.99609375],
            [0.51953125, 0.453125, 0.38671875, 0.99609375],
            [0.84765625, 0.94140625, 0.63671875, 0.99609375],
            [0.30859375, 0.91796875, 0.59375, 0.99609375],
            [0.46484375, 0.76171875, 0.47265625, 0.99609375],
            [0.71875, 0.5390625, 0.546875, 0.99609375],
            [0.40234375, 0.3671875, 0.30859375, 0.99609375],
        ]
    )


def apply_material(obj):
    color = get_random_color()
    mat = bpy.data.materials.new(name="Material")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    mat.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 0

    obj.data.materials.append(mat)


def add_lights():
    bpy.ops.object.light_add(type="SUN")
    bpy.context.object.data.energy = 10


################################################################
# helper functions END
################################################################


def create_circle_control_empty():
    empty = add_ctrl_empty(name=f"empty.circle.cntrl")
    empty.rotation_euler.z = math.radians(random.uniform(0, 360))
    empty.location.z = random.uniform(-3, 1)
    return empty


def animate_object_translation(context, obj):
    frame = random.randint(-context["frame_count"], 0)
    obj.location.x = 0
    obj.keyframe_insert("location", frame=frame)

    frame += context["frame_count"]

    obj.location.x = random.uniform(5, 5.5)
    obj.keyframe_insert("location", frame=frame)

    fcurves = obj.animation_data.action.fcurves
    location_fcurve = fcurves.find("location")
    location_fcurve.modifiers.new(type="CYCLES")

    make_fcurves_linear()


def gen_centerpiece(context):

    for _ in range(500):
        empty = create_circle_control_empty()

        bpy.ops.mesh.primitive_circle_add(radius=0.1, fill_type="TRIFAN")
        circle = active_object()
        circle.parent = empty

        apply_material(circle)

        animate_object_translation(context, circle)


def main():
    """
    Python code to generate an animation loop with circles
    moving from the origin outward
    """
    context = setup_scene()
    gen_centerpiece(context)
    add_lights()


if __name__ == "__main__":
    main()
"""
See YouTube tutorial here: 
"""

import random
import time

import bpy

################################################################
# helper functions BEGIN
################################################################


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
    returns the currently active object
    """
    return bpy.context.active_object


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


def set_fcurve_extrapolation_to_linear():
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


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


def set_scene_props(fps, frame_count):
    """
    Set scene properties
    """
    scene = bpy.context.scene
    scene.frame_end = frame_count

    # set the world background to black
    world = bpy.data.worlds["World"]
    if "Background" in world.node_tree.nodes:
        world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

    scene.render.fps = fps

    scene.frame_current = 1
    scene.frame_start = 1


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


################################################################
# helper functions END
################################################################


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


def update_geo_node_tree(node_tree):
    """
    Adding a Cube Mesh, Subdiv, Triangulate, Edge Split, and Element scale geo node into the
    geo node tree

    Geo Node type names found here
    https://docs.blender.org/api/current/bpy.types.GeometryNode.html
    """
    out_node = node_tree.nodes["Group Output"]

    node_x_location = 0
    node_location_step_x = 300

    mesh_cube_node, node_x_location = create_node(node_tree, "GeometryNodeMeshCube", node_x_location, node_location_step_x)

    subdivide_mesh_node, node_x_location = create_node(node_tree, "GeometryNodeSubdivideMesh", node_x_location, node_location_step_x)
    subdivide_mesh_node.inputs["Level"].default_value = 3

    triangulate_node, node_x_location = create_node(node_tree, "GeometryNodeTriangulate", node_x_location, node_location_step_x)

    split_edges_node, node_x_location = create_node(node_tree, "GeometryNodeSplitEdges", node_x_location, node_location_step_x)

    separate_geometry_node, join_geometry_node, node_x_location = separate_faces_and_animate_scale(node_tree, node_x_location, node_location_step_x)

    out_node.location.x = node_x_location

    link_nodes_by_mesh_socket(node_tree, from_node=mesh_cube_node, to_node=subdivide_mesh_node)
    link_nodes_by_mesh_socket(node_tree, from_node=subdivide_mesh_node, to_node=triangulate_node)
    link_nodes_by_mesh_socket(node_tree, from_node=triangulate_node, to_node=split_edges_node)

    from_node = split_edges_node
    to_node = separate_geometry_node
    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Geometry"])

    from_node = join_geometry_node
    to_node = out_node
    node_tree.links.new(from_node.outputs["Geometry"], to_node.inputs["Geometry"])


def create_centerpiece():
    bpy.ops.mesh.primitive_plane_add()

    bpy.ops.node.new_geometry_nodes_modifier()
    node_tree = bpy.data.node_groups["Geometry Nodes"]

    update_geo_node_tree(node_tree)

    bpy.ops.object.modifier_add(type="SOLIDIFY")

    # make the Geo Nodes modifier the active mode at the end
    bpy.context.active_object.modifiers["GeometryNodes"].is_active = True


def main():
    """
    Python code to generate an animated geo nodes node tree
    that consists of a subdivided & triangulated cube with animated faces
    """
    scene_setup()
    create_centerpiece()


if __name__ == "__main__":
    main()
import math
import random
import time

import bpy

################################################################
# helper functions BEGIN
################################################################


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


def hex_color_to_rgb(hex_color):
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB

    Supports: "#RRGGBB" or "RRGGBB"

    Note: We are converting into Linear RGB since Blender uses a Linear Color Space internally
    https://docs.blender.org/manual/en/latest/render/color_management.html

    Video tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
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


def hex_color_to_rgba(hex_color, alpha=1.0):
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB with an Alpha passed as a parameter

    Supports: "#RRGGBB" or "RRGGBB"

    Video tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    linear_red, linear_green, linear_blue = hex_color_to_rgb(hex_color)
    return tuple([linear_red, linear_green, linear_blue, alpha])


def convert_srgb_to_linear_rgb(srgb_color_component):
    """
    Converting from sRGB to Linear RGB
    based on https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ

    Video tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    if srgb_color_component <= 0.04045:
        linear_color_component = srgb_color_component / 12.92
    else:
        linear_color_component = math.pow((srgb_color_component + 0.055) / 1.055, 2.4)

    return linear_color_component


def active_object():
    """
    returns the active object
    """
    return bpy.context.active_object


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


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

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

    camera.data.dof.use_dof = True
    camera.data.dof.focus_object = empty
    camera.data.dof.aperture_fstop = 0.1

    return empty


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

    scene.eevee.use_bloom = True
    scene.eevee.bloom_intensity = 0.005

    # set Ambient Occlusion properties
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 4
    scene.eevee.gtao_factor = 5

    scene.eevee.taa_render_samples = 64

    scene.view_settings.look = "Very High Contrast"

    set_1080px_square_render_res()


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


def make_fcurves_bounce():
    for fcurve in bpy.context.active_object.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = "BOUNCE"


def render_loop():
    bpy.ops.render.render(animation=True)


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


def get_random_highlight_color():
    hex_color = random.choice(
        [
            "#CB5A0C",
            "#DBF227",
            "#22BABB",
            "#FFEC5C",
        ]
    )
    return hex_color_to_rgb(hex_color)


def add_lights():
    rotation = (math.radians(-60), math.radians(-15), math.radians(-45))

    bpy.ops.object.light_add(type="SUN", rotation=rotation)
    sun_light = active_object()
    sun_light.data.energy = 1.5

    if random.randint(0, 1):
        bpy.ops.object.light_add(type="AREA")
        area_light = active_object()
        area_light.scale *= 5
        area_light.data.color = get_random_highlight_color()
        area_light.data.energy = 200

        euler_x_rotation = math.radians(180)
        z_location = -4
        if random.randint(0, 1):
            euler_x_rotation = 0
            z_location = 4

        area_light.rotation_euler.x = euler_x_rotation
        area_light.location.z = z_location


def create_metallic_material(color):
    material = bpy.data.materials.new(name="metallic.material")
    material.use_nodes = True

    bsdf_node = material.node_tree.nodes["Principled BSDF"]
    bsdf_node.inputs["Base Color"].default_value = color
    bsdf_node.inputs["Metallic"].default_value = 1.0

    return material


def apply_material(obj, material):
    obj.data.materials.append(material)


################################################################
# helper functions END
################################################################


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


def create_bevel(obj):
    # convert mesh into a curve
    bpy.ops.object.convert(target="CURVE")

    # add bevel to curve
    obj.data.bevel_depth = 0.025
    obj.data.bevel_resolution = 16

    # shade smooth
    bpy.ops.object.shade_smooth()


def create_centerpiece(context):
    radius_step = 0.2

    number_of_shapes = 16

    frame_offset = 5

    # repeat number_of_shapes times
    for i in range(1, number_of_shapes):

        # add a mesh into the scene
        current_radius = i * radius_step
        bpy.ops.mesh.primitive_circle_add(vertices=6, radius=current_radius)

        # get a reference to the currently active object
        shape_obj = active_object()

        # rotate mesh about the x-axis
        degrees = -90
        radians = math.radians(degrees)
        shape_obj.rotation_euler.x = radians

        animate_rotation(context, shape_obj, i, frame_offset)

        create_bevel(shape_obj)

        apply_material(shape_obj, context["material"])


def main():
    """
    Python code to generate an abstract delayed rotation animation
    with hexagonal rings
    """
    context = scene_setup()
    create_centerpiece(context)
    add_lights()


if __name__ == "__main__":
    main()

"""
Python code to generate this animation
https://www.artstation.com/artwork/g2A5rZ
"""
import math
import pprint
import random
import time

import addon_utils
import bpy
import mathutils

################################################################
# region helper functions BEGIN
################################################################


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


def clean_scene_experimental():
    """
    This might crash Blender!
    Proceed at your own risk!
    But it will clean the scene.
    """
    old_scene_name = "to_delete"
    bpy.context.window.scene.name = old_scene_name
    bpy.ops.scene.new()
    bpy.data.scenes.remove(bpy.data.scenes[old_scene_name])

    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


def active_object():
    """
    returns the currently active object
    """
    return bpy.context.active_object


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


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

    return empty


def set_1080px_square_render_res():
    """
    Set the resolution of the rendered image to 1080 by 1080
    """
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080


def set_fcurve_extrapolation_to_linear():
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


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


def hex_color_to_rgba(hex_color, alpha=1.0):
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB with an Alpha passed as a parameter

    Supports: "#RRGGBB" or "RRGGBB"

    Video Tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    linear_red, linear_green, linear_blue = hex_color_to_rgb(hex_color)
    return tuple([linear_red, linear_green, linear_blue, alpha])


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


def apply_material(material):
    obj = active_object()
    obj.data.materials.append(material)


def apply_emission_material(color, name=None, energy=1):
    material = create_emission_material(color, name=name, energy=energy)

    obj = active_object()
    obj.data.materials.append(material)


def create_emission_material(color, name=None, energy=30, return_nodes=False):
    if name is None:
        name = ""

    material = bpy.data.materials.new(name=f"material.emission.{name}")
    material.use_nodes = True

    out_node = material.node_tree.nodes.get("Material Output")
    bsdf_node = material.node_tree.nodes.get("Principled BSDF")
    material.node_tree.nodes.remove(bsdf_node)

    node_emission = material.node_tree.nodes.new(type="ShaderNodeEmission")
    node_emission.inputs["Color"].default_value = color
    node_emission.inputs["Strength"].default_value = energy

    node_emission.location = 0, 0

    material.node_tree.links.new(node_emission.outputs["Emission"], out_node.inputs["Surface"])

    if return_nodes:
        return material, material.node_tree.nodes
    else:
        return material


def parent(child_obj, parent_obj, keep_transform=False):
    """
    Parent the child object to the parent object
    """
    make_active(child_obj)
    child_obj.parent = parent_obj
    if keep_transform:
        child_obj.matrix_parent_inverse = parent_obj.matrix_world.inverted()


def add_bezier_circle(radius=1.0, bevel_depth=0.0, resolution_u=12, extrude=0):
    bpy.ops.curve.primitive_bezier_circle_add(radius=radius)

    bezier_circle_obj = active_object()

    bezier_circle_obj.data.bevel_depth = bevel_depth
    bezier_circle_obj.data.resolution_u = resolution_u
    bezier_circle_obj.data.extrude = extrude

    return bezier_circle_obj


def add_round_cube(radius=1.0):
    enable_extra_meshes()
    bpy.ops.mesh.primitive_round_cube_add(radius=radius)
    return active_object()


def add_subdivided_round_cube(radius=1.0):

    round_cube_obj = add_round_cube(radius)

    bpy.ops.object.modifier_add(type="SUBSURF")

    return round_cube_obj, round_cube_obj.modifiers["Subdivision"]


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


def add_fcruve_cycles_modifier(obj=None):
    """
    Apply a cycles modifier to all the fcurve animation data of an object.
    """
    if obj is None:
        obj = active_object()

    for fcurve in obj.animation_data.action.fcurves.values():
        modifier = fcurve.modifiers.new(type="CYCLES")
        modifier.mode_before = "REPEAT"
        modifier.mode_after = "REPEAT"


def animate_up_n_down_bob(start_value, mid_value, obj=None, loop_length=90, start_frame=random.randint(0, 60)):
    """Animate the up and down bobbing motion of an object. Apply a fcurve cycles modifier to make it seamless."""
    if obj is None:
        obj = active_object()

    create_data_animation_loop(
        obj,
        "location",
        start_value=start_value,
        mid_value=mid_value,
        start_frame=start_frame,
        loop_length=loop_length,
        linear_extrapolation=False,
    )

    add_fcruve_cycles_modifier(obj)


def get_random_rotation():
    x = math.radians(random.uniform(0, 360))
    y = math.radians(random.uniform(0, 360))
    z = math.radians(random.uniform(0, 360))
    return mathutils.Euler((x, y, z))


def add_displace_modifier(name, texture_type, empty_obj=None):
    """
    Add a displace modifier and a texture to the currently active object.
    Return the modifier, texture, and empty object to
    control the modifier.
    """
    obj = active_object()

    texture = bpy.data.textures.new(f"texture.{name}", texture_type)

    bpy.ops.object.modifier_add(type="DISPLACE")
    displace_modifier = obj.modifiers["Displace"]
    displace_modifier.texture = texture
    displace_modifier.name = f"displace.{name}"
    displace_modifier.texture_coords = "OBJECT"

    if empty_obj == None:
        empty_obj = add_ctrl_empty()

    empty_obj.name = f"empty.{name}"

    displace_modifier.texture_coords_object = empty_obj

    return displace_modifier, texture, empty_obj


# bpybb end


def load_color_palettes():
    return [
        ["#69D2E7", "#A7DBD8", "#E0E4CC", "#F38630", "#FA6900"],
        ["#FE4365", "#FC9D9A", "#F9CDAD", "#C8C8A9", "#83AF9B"],
        ["#ECD078", "#D95B43", "#C02942", "#542437", "#53777A"],
        ["#556270", "#4ECDC4", "#C7F464", "#FF6B6B", "#C44D58"],
        ["#774F38", "#E08E79", "#F1D4AF", "#ECE5CE", "#C5E0DC"],
        ["#E8DDCB", "#CDB380", "#036564", "#033649", "#031634"],
        ["#490A3D", "#BD1550", "#E97F02", "#F8CA00", "#8A9B0F"],
        ["#594F4F", "#547980", "#45ADA8", "#9DE0AD", "#E5FCC2"],
        ["#00A0B0", "#6A4A3C", "#CC333F", "#EB6841", "#EDC951"],
        ["#E94E77", "#D68189", "#C6A49A", "#C6E5D9", "#F4EAD5"],
        ["#3FB8AF", "#7FC7AF", "#DAD8A7", "#FF9E9D", "#FF3D7F"],
        ["#D9CEB2", "#948C75", "#D5DED9", "#7A6A53", "#99B2B7"],
        ["#FFFFFF", "#CBE86B", "#F2E9E1", "#1C140D", "#CBE86B"],
        ["#343838", "#005F6B", "#008C9E", "#00B4CC", "#00DFFC"],
        ["#EFFFCD", "#DCE9BE", "#555152", "#2E2633", "#99173C"],
        ["#413E4A", "#73626E", "#B38184", "#F0B49E", "#F7E4BE"],
    ]


def select_random_color_palette():
    random_palette = random.choice(load_color_palettes())
    print("Random palette:")
    pprint.pprint(random_palette)
    return random_palette


def get_random_color(color_palette):
    hex_color = random.choice(color_palette)
    return hex_color_to_rgba(hex_color)


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

    focus_empty = add_ctrl_empty(name=f"empty.focus")
    focus_empty.location.z = 0.33
    camera.data.dof.use_dof = True
    camera.data.dof.aperture_fstop = 1.1
    camera.data.dof.focus_object = focus_empty

    return empty


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


def scene_setup(i=0):
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds

    project_name = "holder"
    bpy.context.scene.render.image_settings.file_format = "PNG"

    seed = 0
    if seed:
        random.seed(seed)
    else:
        seed = time_seed()

    bpy.context.scene.render.filepath = f"/tmp/project_{project_name}_{seed}/"

    # Utility Building Blocks
    use_clean_scene_experimental = False
    if use_clean_scene_experimental:
        clean_scene_experimental()
    else:
        clean_scene()

    set_scene_props(fps, loop_seconds)

    loc = (0, 0, 3.5)
    rot = (0, 0, 0)
    setup_camera(loc, rot)

    context = {
        "frame_count": frame_count,
    }

    return context


def add_lights(color_palette):
    """Add lights into the scene"""
    bpy.ops.object.light_add(type="AREA", radius=5, location=(0, 0, -5))
    light = active_object()
    light.data.shape = "DISK"
    light.data.energy = random.choice([200, 300, 500])
    light.rotation_euler.y = math.radians(180)

    bpy.ops.object.light_add(type="AREA", radius=5, location=(0, 0, 5))
    light = active_object()
    light.data.shape = "DISK"
    light.data.energy = 100

    add_bezier_circle(radius=1.5, bevel_depth=0.0, resolution_u=12, extrude=0.1)
    apply_emission_material(get_random_color(color_palette), energy=100)


################################################################
# endregion helper functions END
################################################################


def create_spherical_gradient_tex_mask(material, node_location_step_x, node_y_location):
    """Adds a group of nodes that creates the spherical mask to separate the glass and metallic parts of the material"""
    node_x_location = 0
    texture_coordinate_node = material.node_tree.nodes.new(type="ShaderNodeTexCoord")
    texture_coordinate_node.location = mathutils.Vector((node_x_location, node_y_location))
    node_x_location += node_location_step_x

    mapping_node = material.node_tree.nodes.new(type="ShaderNodeMapping")
    mapping_node.location = mathutils.Vector((node_x_location, node_y_location))
    node_x_location += node_location_step_x

    gradient_texture_node = material.node_tree.nodes.new(type="ShaderNodeTexGradient")
    gradient_texture_node.gradient_type = "SPHERICAL"
    gradient_texture_node.location = mathutils.Vector((node_x_location, node_y_location))
    node_x_location += node_location_step_x

    mix_shader_color_ramp_node = material.node_tree.nodes.new(type="ShaderNodeValToRGB")
    mix_shader_color_ramp_node.color_ramp.elements[1].position = 0.535
    mix_shader_color_ramp_node.color_ramp.interpolation = "CONSTANT"
    mix_shader_color_ramp_node.location = mathutils.Vector((node_x_location, node_y_location))
    node_x_location += node_location_step_x

    material.node_tree.links.new(texture_coordinate_node.outputs["Object"], mapping_node.inputs["Vector"])
    material.node_tree.links.new(mapping_node.outputs["Vector"], gradient_texture_node.inputs["Vector"])
    material.node_tree.links.new(gradient_texture_node.outputs["Color"], mix_shader_color_ramp_node.inputs["Fac"])

    return mix_shader_color_ramp_node, node_x_location


def create_pointiness_edge_highlight_node_tree(color_palette, material, node_location_step_x, node_y_location):
    """Adds a group of nodes that highlights the edges of the Voronoi displacement
    part of the main material"""
    node_x_location = 0
    geometry_node = material.node_tree.nodes.new(type="ShaderNodeNewGeometry")
    geometry_node.location = mathutils.Vector((node_x_location, node_y_location))
    node_x_location += node_location_step_x

    color_ramp_node = material.node_tree.nodes.new(type="ShaderNodeValToRGB")
    color_ramp_node.color_ramp.elements[0].color = (1, 1, 1, 1)
    color_ramp_node.color_ramp.elements[1].color = (0, 0, 0, 1)
    color_ramp_node.color_ramp.elements[1].position = 0.5
    color_ramp_node.color_ramp.interpolation = "CONSTANT"
    color_ramp_node.location = mathutils.Vector((node_x_location, node_y_location))
    node_x_location += node_location_step_x

    material.node_tree.links.new(geometry_node.outputs["Pointiness"], color_ramp_node.inputs["Fac"])

    mix_rgb_node = material.node_tree.nodes.new(type="ShaderNodeMix")
    mix_rgb_node_input_lookup = {socket.identifier: socket for socket in mix_rgb_node.inputs.values()}
    mix_rgb_node_output_lookup = {socket.identifier: socket for socket in mix_rgb_node.outputs.values()}
    mix_rgb_node.data_type = "RGBA"
    mix_rgb_node.blend_type = "MIX"
    mix_rgb_node.location = mathutils.Vector((node_x_location, node_y_location))

    try_count = 5
    color_a = get_random_color(color_palette)
    color_b = get_random_color(color_palette)
    while color_b == color_a and try_count > 0:
        color_b = get_random_color(color_palette)
        try_count -= 1

    mix_rgb_node_input_lookup["A_Color"].default_value = color_a
    mix_rgb_node_input_lookup["B_Color"].default_value = color_b
    node_x_location += node_location_step_x

    material.node_tree.links.new(color_ramp_node.outputs["Color"], mix_rgb_node_input_lookup["Factor_Float"])

    return mix_rgb_node_output_lookup["Result_Color"], node_x_location


def create_glass_node_tree(color_palette, material, node_location_step_x, node_x_location, node_y_location):
    """Adds a group of nodes that creates the glass part of the main material"""

    layer_weight_node = material.node_tree.nodes.new(type="ShaderNodeLayerWeight")
    layer_weight_node.location = mathutils.Vector((node_x_location, node_y_location))
    node_x_location += node_location_step_x

    base_color = get_random_color(color_palette)

    color_ramp_node = material.node_tree.nodes.new(type="ShaderNodeValToRGB")
    color_ramp_node.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_node.color_ramp.elements[0].position = 0.78
    color_ramp_node.color_ramp.elements[1].color = base_color
    color_ramp_node.color_ramp.elements[1].position = 1.00
    color_ramp_node.location = mathutils.Vector((node_x_location, node_y_location))
    node_x_location += node_location_step_x

    material.node_tree.links.new(layer_weight_node.outputs["Facing"], color_ramp_node.inputs["Fac"])

    principled_bsdf_node = material.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
    principled_bsdf_node.inputs["Base Color"].default_value = base_color
    principled_bsdf_node.inputs["Metallic"].default_value = 0.0
    principled_bsdf_node.inputs["Specular"].default_value = 0.0
    principled_bsdf_node.inputs["Roughness"].default_value = 0.25
    principled_bsdf_node.inputs["Transmission"].default_value = 1.0
    principled_bsdf_node.inputs["Emission Strength"].default_value = 15.0
    principled_bsdf_node.hide = True
    principled_bsdf_node.location = mathutils.Vector((node_x_location, node_y_location))

    material.node_tree.links.new(color_ramp_node.outputs["Color"], principled_bsdf_node.inputs["Emission"])

    return principled_bsdf_node


def create_metallic_node_tree(color_palette, material, node_location_step_x):
    """Adds a group of nodes that creates the metallic part of the main material"""

    result = create_spherical_gradient_tex_mask(material, node_location_step_x, node_y_location=300)
    mix_shader_color_ramp_node, spherical_gradient_x_location = result

    result = create_pointiness_edge_highlight_node_tree(color_palette, material, node_location_step_x, node_y_location=-100)
    mix_rgb_node_output_color, edge_highlight_x_location = result

    node_x_location = max(spherical_gradient_x_location, edge_highlight_x_location)

    principled_bsdf_node = material.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
    principled_bsdf_node.inputs["Metallic"].default_value = 0.54
    principled_bsdf_node.inputs["Roughness"].default_value = 0.26
    principled_bsdf_node.hide = True
    principled_bsdf_node.location = mathutils.Vector((node_x_location, 0))

    material.node_tree.links.new(mix_rgb_node_output_color, principled_bsdf_node.inputs["Base Color"])

    return principled_bsdf_node, mix_shader_color_ramp_node, node_x_location


def create_material(color_palette):
    """Creates and configures all the shader nodes for the centerpiece material"""
    material = bpy.data.materials.new(name="glass_plus_metallic_voronoi")
    material.use_nodes = True

    # remove all nodes
    material.node_tree.nodes.clear()

    node_location_step_x = 300
    node_x_location = 0

    principled_bsdf_node, mix_shader_color_ramp_node, node_x_location = create_metallic_node_tree(color_palette, material, node_location_step_x)

    principled_bsdf_glass_node = create_glass_node_tree(color_palette, material, node_location_step_x, node_x_location=600, node_y_location=-600)

    node_x_location += node_location_step_x

    mix_shader_node = material.node_tree.nodes.new(type="ShaderNodeMixShader")
    mix_shader_node_input_lookup = {socket.identifier: socket for socket in mix_shader_node.inputs.values()}
    mix_shader_node.location = mathutils.Vector((node_x_location, 100))
    node_x_location += node_location_step_x

    material_output = material.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
    material_output.location = mathutils.Vector((node_x_location, 0))

    material.node_tree.links.new(mix_shader_color_ramp_node.outputs["Color"], mix_shader_node_input_lookup["Fac"])
    material.node_tree.links.new(principled_bsdf_node.outputs["BSDF"], mix_shader_node_input_lookup["Shader"])
    material.node_tree.links.new(principled_bsdf_glass_node.outputs["BSDF"], mix_shader_node_input_lookup["Shader_001"])
    material.node_tree.links.new(mix_shader_node.outputs["Shader"], material_output.inputs["Surface"])

    return material


def create_mesh(ctrl_empty, radius=1.0):
    round_cube, subdivision_modifier = add_subdivided_round_cube(radius)

    parent(round_cube, ctrl_empty)

    subdivision_modifier.levels = 5
    subdivision_modifier.render_levels = 7
    bpy.ops.object.shade_smooth()


def animate_displace_modifier(context):
    displace_modifier, texture, empty = add_displace_modifier(name="base_noise", texture_type="VORONOI")
    texture.noise_scale = 0.75
    texture.noise_intensity = 1
    texture.intensity = 0.4
    texture.use_clamp = True

    loop_circle_path = add_bezier_circle(0.2)
    loop_circle_path.name = "loop_circle_path"
    loop_circle_path.data.path_duration = context["frame_count"]

    make_active(empty)

    empty.rotation_euler = get_random_rotation()

    bpy.ops.object.constraint_add(type="FOLLOW_PATH")
    empty.constraints["Follow Path"].target = loop_circle_path
    bpy.ops.constraint.followpath_path_animate(constraint="Follow Path", owner="OBJECT")


def create_centerpiece(context):
    ctrl_empty = add_ctrl_empty()

    create_mesh(ctrl_empty)

    material = create_material(context["color_palette"])
    apply_material(material)

    start_value = mathutils.Vector((0, 0, 0.05))
    mid_value = mathutils.Vector((0, 0, -0.05))
    animate_up_n_down_bob(obj=ctrl_empty, start_value=start_value, mid_value=mid_value)

    animate_displace_modifier(context)


def main():
    """
    Python code to generate this animation
    https://www.artstation.com/artwork/g2A5rZ
    """
    context = scene_setup()
    context["color_palette"] = select_random_color_palette()
    create_centerpiece(context)
    add_lights(context["color_palette"])


if __name__ == "__main__":
    main()

import math
import random
import time

import bpy

################################################################
# helper functions BEGIN
################################################################


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


def clean_scene_experimental():
    """
    This might crash Blender!
    Proceed at your own risk!
    But it will clean the scene.
    """
    old_scene_name = "to_delete"
    bpy.context.window.scene.name = old_scene_name
    bpy.ops.scene.new()
    bpy.data.scenes.remove(bpy.data.scenes[old_scene_name])

    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


def active_object():
    """
    returns the currently active object
    """
    return bpy.context.active_object


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


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

    return empty


def set_1080px_square_render_res():
    """
    Set the resolution of the rendered image to 1080 by 1080
    """
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080


def set_fcurve_extrapolation_to_linear():
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


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


def hex_color_to_rgba(hex_color, alpha=1.0):
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB with an Alpha passed as a parameter

    Supports: "#RRGGBB" or "RRGGBB"

    Video Tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    linear_red, linear_green, linear_blue = hex_color_to_rgb(hex_color)
    return tuple([linear_red, linear_green, linear_blue, alpha])


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


def animate_360_rotation(axis_index, last_frame, obj=None, clockwise=False, linear=True, start_frame=1):
    animate_rotation(360, axis_index, last_frame, obj, clockwise, linear, start_frame)


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


def create_emission_material(color, name=None, energy=30, return_nodes=False):
    if name is None:
        name = ""

    material = bpy.data.materials.new(name=f"material.emission.{name}")
    material.use_nodes = True

    out_node = material.node_tree.nodes.get("Material Output")
    bsdf_node = material.node_tree.nodes.get("Principled BSDF")
    material.node_tree.nodes.remove(bsdf_node)

    node_emission = material.node_tree.nodes.new(type="ShaderNodeEmission")
    node_emission.inputs["Color"].default_value = color
    node_emission.inputs["Strength"].default_value = energy

    node_emission.location = 0, 0

    material.node_tree.links.new(node_emission.outputs["Emission"], out_node.inputs["Surface"])

    if return_nodes:
        return material, material.node_tree.nodes
    else:
        return material


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


def apply_reflective_material(color, name=None, roughness=0.1, specular=0.5):
    material = create_reflective_material(color, name=name, roughness=roughness, specular=specular)

    obj = active_object()
    obj.data.materials.append(material)


def render_loop():
    bpy.ops.render.render(animation=True)


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
    # scene.cycles.device = 'GPU'

    # Use the CPU to render
    scene.cycles.device = "CPU"

    scene.cycles.samples = 1024

    scene.view_settings.look = "Very High Contrast"

    set_1080px_square_render_res()


def scene_setup(i=0):
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds

    project_name = "in_or_out"
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

    loc = (0, 0, 7)
    rot = (0, 0, 0)
    setup_camera(loc, rot)

    context = {
        "frame_count": frame_count,
    }

    return context


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


################################################################
# helper functions END
################################################################


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


def create_metaball(path):
    bpy.ops.object.metaball_add()
    ball = active_object()
    ball.data.render_resolution = 0.05
    ball.scale *= random.uniform(0.05, 0.5)

    bpy.ops.object.constraint_add(type="FOLLOW_PATH")
    bpy.context.object.constraints["Follow Path"].target = path
    bpy.ops.constraint.followpath_path_animate(constraint="Follow Path", owner="OBJECT")


def create_centerpiece(context):
    metaball_count = 10

    for _ in range(metaball_count):
        path = create_metaball_path(context)
        create_metaball(path)

    apply_metaball_material()


def create_background():
    bpy.ops.curve.primitive_bezier_circle_add(radius=1.5)
    bpy.context.object.data.resolution_u = 64
    bpy.context.object.data.bevel_depth = 0.05

    color = get_random_color()
    apply_emission_material(color, energy=30)


def main():
    """
    Python code to generate this animation
    https://www.artstation.com/artwork/KO66oG
    """
    context = scene_setup()
    create_centerpiece(context)
    create_background()
    add_light()
    apply_glare_composite_effect()


if __name__ == "__main__":
    main()

import math
import random
import time

import bpy

################################################################
# helper functions BEGIN
################################################################


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


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def apply_material(material):
    obj = active_object()
    obj.data.materials.append(material)


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

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


def set_1080px_square_render_res():
    """
    Set the resolution of the rendered image to 1080 by 1080
    """
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080


def make_fcurves_linear():
    for fcurve in bpy.context.active_object.animation_data.action.fcurves:
        for points in fcurve.keyframe_points:
            points.interpolation = "LINEAR"


def get_random_color():
    return random.choice(
        [
            [0.984375, 0.4609375, 0.4140625, 1.0],
            [0.35546875, 0.515625, 0.69140625, 1.0],
            [0.37109375, 0.29296875, 0.54296875, 1.0],
            [0.8984375, 0.6015625, 0.55078125, 1.0],
            [0.2578125, 0.9140625, 0.86328125, 1.0],
            [0.80078125, 0.70703125, 0.59765625, 1.0],
            [0.0, 0.640625, 0.796875, 1.0],
            [0.97265625, 0.33984375, 0.0, 1.0],
            [0.0, 0.125, 0.24609375, 1.0],
            [0.67578125, 0.93359375, 0.81640625, 1.0],
            [0.375, 0.375, 0.375, 1.0],
            [0.8359375, 0.92578125, 0.08984375, 1.0],
            [0.92578125, 0.16796875, 0.19921875, 1.0],
            [0.84375, 0.3515625, 0.49609375, 1.0],
            [0.58984375, 0.734375, 0.3828125, 1.0],
            [0.0, 0.32421875, 0.609375, 1.0],
            [0.9296875, 0.640625, 0.49609375, 1.0],
            [0.0, 0.38671875, 0.6953125, 1.0],
            [0.609375, 0.76171875, 0.83203125, 1.0],
            [0.0625, 0.09375, 0.125, 1.0],
        ]
    )


def render_loop():
    bpy.ops.render.render(animation=True)


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
    # add a plain into the scene
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -6.0))
    floor_obj = active_object()
    floor_obj.name = "plane.floor"

    # create and assign an emissive material
    floor_material = create_floor_material()
    floor_obj.data.materials.append(floor_material)


def add_light():
    # add area light
    bpy.ops.object.light_add(type="AREA")
    area_light = active_object()

    # update scale and location
    area_light.location.z = 6
    area_light.scale *= 10

    # set the light's energy
    area_light.data.energy = 1000


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
    # scene.cycles.device = 'GPU'
    # scene.cycles.samples = 1024

    # Use the CPU to render
    scene.cycles.device = "CPU"
    scene.cycles.samples = 200

    if bpy.app.version < (4, 0, 0):
        scene.view_settings.look = "Very High Contrast"
    else:
        scene.view_settings.look = "AgX - Very High Contrast"

    set_1080px_square_render_res()


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


################################################################
# helper functions END
################################################################


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


def create_ring(index, current_radius, ring_material):
    # add a circle mesh into the scene
    bpy.ops.mesh.primitive_circle_add(vertices=128, radius=current_radius)

    # get a reference to the currently active object
    ring_obj = bpy.context.active_object
    ring_obj.name = f"ring.{index}"

    # convert mesh into a curve
    bpy.ops.object.convert(target="CURVE")

    # add bevel to curve
    ring_obj.data.bevel_depth = 0.05
    ring_obj.data.bevel_resolution = 16

    # shade smooth
    bpy.ops.object.shade_smooth()

    # apply the material
    apply_material(ring_material)

    return ring_obj


def create_centerpiece(context):
    # create variables used in the loop
    radius_step = 0.1
    number_rings = 50

    z_rotation_step = 10
    z_rotation = 0

    y_rotation = 30

    ring_material = create_metal_ring_material()

    # repeat 50 times
    for i in range(number_rings):

        # calculate new radius
        current_radius = radius_step * i

        ring_obj = create_ring(i, current_radius, ring_material)

        # rotate ring and inset keyframes
        animate_rotation(context, ring_obj, z_rotation, y_rotation)

        # update the z-axis rotation
        z_rotation = z_rotation + z_rotation_step


def main():
    """
    Python code that creates an abstract ring animation loop
    """
    context = setup_scene()
    create_centerpiece(context)
    create_background()
    add_light()


if __name__ == "__main__":
    main()

import math
import pathlib
import random
import time

import addon_utils
import bpy

################################################################
# helper functions BEGIN
################################################################


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


def clean_scene_experimental():
    """
    This might crash Blender!
    Proceed at your own risk!
    But it will clean the scene.
    """
    old_scene_name = "to_delete"
    bpy.ops.scene.new()
    bpy.data.scenes.remove(bpy.data.scenes[old_scene_name])

    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


def active_object():
    """
    returns the currently active object
    """
    return bpy.context.active_object


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


def add_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

    return empty


def set_1080px_square_render_res():
    """
    Set the resolution of the rendered image to 1080 by 1080
    """
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080


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


def hex_color_to_rgba(hex_color, alpha=1.0):
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB with an Alpha passed as a parameter

    Supports: "#RRGGBB" or "RRGGBB"

    Video Tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    linear_red, linear_green, linear_blue = hex_color_to_rgb(hex_color)
    return tuple([linear_red, linear_green, linear_blue, alpha])


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


def parent(child_obj, parent_obj, keep_transform=False):
    """
    Parent the child object to the parent object

    Args:
        child_obj: child object that will be parented.
        parent_obj: parent object that will be parented to.
        keep_transform: keep the transform of the child object. Defaults to False.
    """
    make_active(child_obj)
    child_obj.parent = parent_obj
    if keep_transform:
        child_obj.matrix_parent_inverse = parent_obj.matrix_world.inverted()


def apply_material(material):
    obj = active_object()
    obj.data.materials.append(material)


def set_fcurve_extrapolation_to_linear(obj=None):
    """loops over all the fcurves of an action
    and sets the extrapolation to "LINEAR"
    """
    if obj is None:
        obj = active_object()

    for fc in obj.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


def apply_hdri(path_to_image, bg_color, hdri_light_strength, bg_strength):
    """
    Based on a technique from a FlippedNormals tutorial
    https://www.youtube.com/watch?v=dbAWTNCJVEs
    """
    world_node_tree = bpy.context.scene.world.node_tree
    world_node_tree.nodes.clear()

    location_x = 0

    texture_coordinate_node = world_node_tree.nodes.new(type="ShaderNodeTexCoord")
    texture_coordinate_node.location.x = location_x
    location_x += 200

    mapping_node = world_node_tree.nodes.new(type="ShaderNodeMapping")
    mapping_node.location.x = location_x
    location_x += 200

    environment_texture_node = world_node_tree.nodes.new(type="ShaderNodeTexEnvironment")
    environment_texture_node.location.x = location_x
    location_x += 300
    environment_texture_node.image = bpy.data.images.load(path_to_image)

    background_node = world_node_tree.nodes.new(type="ShaderNodeBackground")
    background_node.location.x = location_x
    background_node.inputs["Strength"].default_value = hdri_light_strength

    background_node_2 = world_node_tree.nodes.new(type="ShaderNodeBackground")
    background_node_2.location.x = location_x
    background_node_2.location.y = -100
    background_node_2.inputs["Color"].default_value = bg_color
    background_node_2.inputs["Strength"].default_value = bg_strength

    light_path_node = world_node_tree.nodes.new(type="ShaderNodeLightPath")
    light_path_node.location.x = location_x
    light_path_node.location.y = 400
    location_x += 200

    mix_shader_node = world_node_tree.nodes.new(type="ShaderNodeMixShader")
    mix_shader_node.location.x = location_x
    location_x += 200

    world_output_node = world_node_tree.nodes.new(type="ShaderNodeOutputWorld")
    world_output_node.location.x = location_x
    location_x += 200

    # links begin
    from_node = background_node
    to_node = mix_shader_node
    world_node_tree.links.new(from_node.outputs["Background"], to_node.inputs["Shader"])

    from_node = mapping_node
    to_node = environment_texture_node
    world_node_tree.links.new(from_node.outputs["Vector"], to_node.inputs["Vector"])

    from_node = texture_coordinate_node
    to_node = mapping_node
    world_node_tree.links.new(from_node.outputs["Generated"], to_node.inputs["Vector"])

    from_node = environment_texture_node
    to_node = background_node
    world_node_tree.links.new(from_node.outputs["Color"], to_node.inputs["Color"])

    from_node = background_node_2
    to_node = mix_shader_node
    world_node_tree.links.new(from_node.outputs["Background"], to_node.inputs[2])

    from_node = light_path_node
    to_node = mix_shader_node
    world_node_tree.links.new(from_node.outputs["Is Camera Ray"], to_node.inputs["Fac"])

    from_node = mix_shader_node
    to_node = world_output_node
    world_node_tree.links.new(from_node.outputs["Shader"], to_node.inputs["Surface"])

    return world_node_tree


def animate_360_rotation(axis_index, last_frame, obj=None, clockwise=False, linear=True, start_frame=1):
    animate_rotation(360, axis_index, last_frame, obj, clockwise, linear, start_frame)


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


def enable_extra_curves():
    """
    Add Curve Extra Objects
    https://docs.blender.org/manual/en/latest/addons/add_curve/extra_objects.html
    """
    loaded_default, loaded_state = addon_utils.check("add_curve_extra_objects")
    if not loaded_state:
        addon_utils.enable("add_curve_extra_objects")


def setup_camera(frame_count):
    """
    create and setup the camera
    """
    bpy.ops.object.camera_add()
    camera = active_object()

    start_location = (-0.5, 7, 0)
    camera.location = start_location
    mid_location = (-0.5, 8.5, 1.5)
    create_data_animation_loop(camera, "location", start_location, mid_location, start_frame=1, loop_length=frame_count, linear_extrapolation=False)

    # set the camera as the "active camera" in the scene
    bpy.context.scene.camera = camera

    # set the Focal Length of the camera
    camera.data.lens = 70
    camera.data.dof.use_dof = True
    camera.data.dof.aperture_fstop = 1.1

    camera.data.passepartout_alpha = 0.9

    empty = track_empty(camera)

    camera.data.dof.focus_object = empty

    return empty


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


def scene_setup(i=0):
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds

    project_name = "outline"
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

    loop_frame_count = frame_count + 1
    setup_camera(loop_frame_count)

    context = {"frame_count": frame_count, "loop_frame_count": loop_frame_count}

    return context


def add_lights():
    """
    I used this HDRI: https://polyhaven.com/a/studio_small_03

    Please consider supporting polyhaven.com @ https://www.patreon.com/polyhaven/overview
    """
    # update the path to where you downloaded the HDRI
    path_to_image = str(pathlib.Path.home() / "tmp" / "studio_small_03_1k.exr")

    color = get_random_color()
    apply_hdri(path_to_image, bg_color=color, hdri_light_strength=1, bg_strength=1)


def render_loop():
    bpy.ops.render.render(animation=True)


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


################################################################
# helper functions END
################################################################


def create_bevel_obj():
    bpy.ops.curve.primitive_bezier_circle_add(radius=0.05, enter_editmode=False)
    return active_object()


def add_curve(last_frame, bevel_obj, material):
    curve_ctrl = add_empty()
    curve_ctrl.rotation_euler.x = math.radians(90)
    curve_ctrl.rotation_euler.z = math.radians(45)

    bpy.ops.curve.simple(Simple_Type="Arc", Simple_endangle=120, edit_mode=False, use_cyclic_u=False)
    curve = active_object()

    apply_material(material)

    curve.location.y = -0.25

    curve.data.bevel_mode = "OBJECT"
    curve.data.bevel_object = bevel_obj
    curve.data.resolution_u = 32
    curve.data.use_fill_caps = True

    animate_360_rotation(Axis.Z, last_frame, obj=curve, clockwise=False, linear=True, start_frame=1)

    parent(curve, curve_ctrl)

    return curve_ctrl


def create_centerpiece(context):

    count = 32
    rotation_step = 360 / count

    current_rotation = 0

    bevel_obj = create_bevel_obj()

    material = create_metallic_material(get_random_color(), name="curve", roughness=0.1)

    for _ in range(count):
        rotation_ctrl = add_empty()
        rotation_ctrl.rotation_euler.y = math.radians(current_rotation)

        curve_ctrl = add_curve(context["loop_frame_count"], bevel_obj, material)
        parent(curve_ctrl, rotation_ctrl)

        current_rotation += rotation_step


def main():
    """
    Python code to generate this animation
    https://www.artstation.com/artwork/klEGRy
    """
    enable_extra_curves()

    context = scene_setup()
    create_centerpiece(context)
    add_lights()


if __name__ == "__main__":
    main()

import os
import pprint
from datetime import datetime

import bpy


def clean_sequencer(sequence_editor_area):
    with bpy.context.temp_override(area=sequence_editor_area):
        bpy.ops.sequencer.select_all(action="SELECT")
        bpy.ops.sequencer.delete()


def find_sequence_editor():
    for area in bpy.context.window.screen.areas:
        if area.type == "SEQUENCE_EDITOR":
            return area
    return None


def get_image_files(image_folder_path, image_extention=".png"):
    image_files = list()
    for file_name in os.listdir(image_folder_path):
        if file_name.endswith(image_extention):
            image_files.append(file_name)
    image_files.sort()

    pprint.pprint(image_files)

    return image_files


def get_image_dimensions(image_path):
    image = bpy.data.images.load(image_path)
    width, height = image.size
    return width, height


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


def gen_video_from_images(image_folder_path, fps):

    image_files = get_image_files(image_folder_path)

    set_up_output_params(image_folder_path, image_files, fps)

    sequence_editor_area = find_sequence_editor()

    clean_sequencer(sequence_editor_area)

    file_info = list()
    for image_name in image_files:
        file_info.append({"name": image_name})

    with bpy.context.temp_override(area=sequence_editor_area):
        bpy.ops.sequencer.image_strip_add(
            directory=image_folder_path + os.sep,
            files=file_info,
            frame_start=1,
        )

    bpy.ops.render.render(animation=True)


def main():
    """
    Python code to generate a mp4 video for a folder with png(s)
    """
    image_folder_path = "C:\\tmp\\day334_3"

    # uncomment the next two lines when running on macOS or Linux
    # user_folder = os.path.expanduser("~")
    # image_folder_path = f"{user_folder}/tmp/my_rendered_frames"

    fps = 30
    gen_video_from_images(image_folder_path, fps)


if __name__ == "__main__":
    main()

import datetime
import os
import shutil

import bpy


def clean_sequencer(sequence_context):
    bpy.ops.sequencer.select_all(sequence_context, action="SELECT")
    bpy.ops.sequencer.delete(sequence_context)


def find_sequence_editor():
    for area in bpy.context.window.screen.areas:
        if area.type == "SEQUENCE_EDITOR":
            return area
    return None


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


def create_transition_between_videos(video_folder_path, fps, clip_length_sec, video_names, clip_middle_offset):

    sequence_editor = find_sequence_editor()

    sequence_editor_context = {
        "area": sequence_editor,
    }
    clean_sequencer(sequence_editor_context)
    clean_proxies(video_folder_path)

    clip_frame_count = clip_length_sec * fps

    start_frame_pos = 0
    clip_transition_overlap = 1 * fps
    for file_name in os.listdir(video_folder_path):
        if file_name not in video_names:
            continue

        video_name = file_name

        # create a full path to the video
        video_path = os.path.join(video_folder_path, video_name)
        print(f"Processing video {video_path}")

        # add video to the sequence editor
        bpy.ops.sequencer.movie_strip_add(
            sequence_editor_context,
            filepath=video_path,
            directory=video_folder_path + os.sep,
            sound=False,
        )

        # get the middle of the clip
        mid_frame = int(bpy.context.active_sequence_strip.frame_final_duration / 2)

        # apply custom offset
        if clip_middle_offset.get(video_name):
            mid_frame += clip_middle_offset.get(video_name)

        clip_start_offset_frame = mid_frame - clip_frame_count

        trim_the_video(clip_start_offset_frame, clip_frame_count)

        move_the_clip_into_position(start_frame_pos, clip_start_offset_frame)

        # if this is not the first clip in the sequence, add a "fade in" transition
        if start_frame_pos != 0:
            apply_fade_in_to_clip(clip_transition_overlap)

        # update the starting position for the next clip
        start_frame_pos = bpy.context.active_sequence_strip.frame_final_end

    # Set the final frame
    bpy.context.scene.frame_end = bpy.context.active_sequence_strip.frame_final_end

    # Render the clip sequence
    # bpy.ops.render.render(animation=True)


def main():
    """
    Python code to create short clips from videos and stich them back to back
    with a transition
    """

    video_folder_path = r"C:\tmp\my_videos"

    # uncomment the next two lines when running on macOS or Linux
    # user_folder = os.path.expanduser("~")
    # video_folder_path = f"{user_folder}/tmp/my_videos"

    set_up_output_params(video_folder_path)

    video_names = [
        "video_01.mp4",
        "video_02.mp4",
        "video_03.mp4",
        "video_04.mp4",
    ]

    fps = 30
    clip_middle_offset = {
        "video_01.mp4": 8 * fps,
        "video_03.mp4": 4 * fps,
    }

    # The length of the clips in seconds
    clip_length_sec = 4

    create_transition_between_videos(video_folder_path, fps, clip_length_sec, video_names, clip_middle_offset)


if __name__ == "__main__":
    main()

import contextlib
import math
import random
import time

import bpy
import mathutils

################################################################
# helper functions BEGIN
################################################################


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


def clean_scene_experimental():
    """
    This might crash Blender!
    Proceed at your own risk!
    But it will clean the scene.
    """
    old_scene_name = "to_delete"
    bpy.context.window.scene.name = old_scene_name
    bpy.ops.scene.new()
    bpy.data.scenes.remove(bpy.data.scenes[old_scene_name])

    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


def active_object():
    """
    returns the currently active object
    """
    return bpy.context.active_object


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


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

    return empty


def set_1080px_square_render_res():
    """
    Set the resolution of the rendered image to 1080 by 1080
    """
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080


def set_fcurve_extrapolation_to_linear():
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


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


def hex_color_to_rgba(hex_color, alpha=1.0):
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB with an Alpha passed as a parameter

    Supports: "#RRGGBB" or "RRGGBB"

    Video Tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    linear_red, linear_green, linear_blue = hex_color_to_rgb(hex_color)
    return tuple([linear_red, linear_green, linear_blue, alpha])


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


def create_base_material():
    material = bpy.data.materials.new(name=f"material.base")
    material.use_nodes = True

    # get a reference to the Principled BSDF node
    bsdf_node = material.node_tree.nodes.get("Principled BSDF")

    object_info_node = material.node_tree.nodes.new(type="ShaderNodeObjectInfo")
    object_info_node.location = mathutils.Vector((-800, 180))
    object_info_node.name = "Object Info"

    color_ramp_node = material.node_tree.nodes.new(type="ShaderNodeValToRGB")
    color_ramp_node.location = mathutils.Vector((-500, 150))
    color_ramp_node.name = "ColorRamp"
    color_ramp_node.color_ramp.interpolation = "LINEAR"

    # make the links between the nodes
    from_node = material.node_tree.nodes.get("Object Info")
    to_node = material.node_tree.nodes.get("ColorRamp")
    material.node_tree.links.new(from_node.outputs["Random"], to_node.inputs["Fac"])
    from_node = material.node_tree.nodes.get("ColorRamp")
    to_node = bsdf_node
    material.node_tree.links.new(from_node.outputs["Color"], to_node.inputs["Base Color"])
    material.node_tree.links.new(from_node.outputs["Color"], to_node.inputs["Roughness"])

    return material, material.node_tree.nodes


def render_loop():
    bpy.ops.render.render(animation=True)


def setup_camera(loc, rot):
    """
    create and setup the camera
    """
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    camera = active_object()

    # set the camera as the "active camera" in the scene
    bpy.context.scene.camera = camera

    # set the Focal Length of the camera
    camera.data.lens = 14

    camera.data.passepartout_alpha = 0.9

    empty = track_empty(camera)

    return empty


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
    scene.cycles.device = 'GPU'

    scene.cycles.samples = 300

    scene.view_settings.look = "Very High Contrast"

    set_1080px_square_render_res()


def scene_setup(i=0):
    fps = 30
    loop_seconds = 3
    frame_count = fps * loop_seconds

    project_name = "shapeshifting"
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

    loc = (1.5, -1.5, 1.5)
    rot = (0, 0, 0)
    setup_camera(loc, rot)

    context = {
        "frame_count": frame_count,
    }

    return context


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


def subdivide(number_cuts=1, smoothness=0):
    with edit_mode():
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.subdivide(number_cuts=number_cuts, smoothness=smoothness)


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


################################################################
# helper functions END
################################################################


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


def create_base_mesh(context, name, size):

    bpy.ops.mesh.primitive_cube_add(size=size)
    mesh_instance = active_object()
    mesh_instance.name = name

    subdivide(number_cuts=5)

    create_cast_to_sphere_animation_loop(context, mesh_instance)

    return mesh_instance


def create_mesh_instance(context):
    mesh_instance = create_base_mesh(context, name="mesh_instance", size=0.18)

    bpy.ops.object.shade_smooth()

    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].segments = 16
    bpy.context.object.modifiers["Bevel"].width = 0.01

    material, nodes = create_base_material()
    mesh_instance.data.materials.append(material)

    colors = context["colors"]
    make_color_ramp_stops_from_colors(nodes["ColorRamp"].color_ramp, colors)

    return mesh_instance


def create_primary_mesh(context):

    obj = create_base_mesh(context, name="primary_mesh", size=2)

    obj.instance_type = "VERTS"
    obj.show_instancer_for_viewport = False
    obj.show_instancer_for_render = False

    return obj


def create_centerpiece(context):

    mesh_instance = create_mesh_instance(context)
    primary_mesh = create_primary_mesh(context)

    mesh_instance.parent = primary_mesh


def get_colors():
    colors = [
        "#A61B34",
        "#D9B18F",
        "#D9CBBF",
        "#732C02",
        "#A66E4E",
    ]
    return [hex_color_to_rgba(color) for color in colors]


def main():
    """
    Python code to generate this animation
    https://www.artstation.com/artwork/3dYDRg
    """
    context = scene_setup()
    context["colors"] = get_colors()
    create_centerpiece(context)
    add_light()


if __name__ == "__main__":
    main()

"""
See YouTube tutorial here: https://youtu.be/56hht5bMy3A
"""
import math
import random
import time

import addon_utils
import bpy

################################################################
# helper functions BEGIN
################################################################


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


def clean_scene_experimental():
    """
    This might crash Blender!
    Proceed at your own risk!
    But it will clean the scene.
    """
    old_scene_name = "to_delete"
    bpy.context.window.scene.name = old_scene_name
    bpy.ops.scene.new()
    bpy.data.scenes.remove(bpy.data.scenes[old_scene_name])

    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


def active_object():
    """
    returns the currently active object
    """
    return bpy.context.active_object


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


def add_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

    return empty


def set_1080px_square_render_res():
    """
    Set the resolution of the rendered image to 1080 by 1080
    """
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080


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


def hex_color_to_rgba(hex_color, alpha=1.0):
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB with an Alpha passed as a parameter

    Supports: "#RRGGBB" or "RRGGBB"

    Video Tutorial: https://www.youtube.com/watch?v=knc1CGBhJeU
    """
    linear_red, linear_green, linear_blue = hex_color_to_rgb(hex_color)
    return tuple([linear_red, linear_green, linear_blue, alpha])


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


def enable_mod_tools():
    """
    enable Modifier Tools addon
    https://docs.blender.org/manual/en/3.0/addons/add_mesh/ant_landscape.html
    """
    enable_addon(addon_module_name="space_view3d_modifier_tools")


def get_random_color():
    hex_color = random.choice(
        [
            "#402217",
            "#515559",
            "#727273",
            "#8C593B",
            "#A64E1B",
            "#A65D05",
            "#A68A80",
            "#A6A6A6",
            "#BF6415",
            "#BF8B2A",
            "#C5992E",
            "#E8BB48",
            "#F2DC6B",
        ]
    )

    return hex_color_to_rgba(hex_color)


def setup_camera(loc, rot):
    """
    create and setup the camera
    """
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    camera = active_object()

    # set the camera as the "active camera" in the scene
    bpy.context.scene.camera = camera

    # set the Focal Length of the camera
    camera.data.lens = 65

    camera.data.passepartout_alpha = 0.9

    empty = track_empty(camera)

    return empty


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


def apply_metallic_material(color, name=None, roughness=0.1):
    material = create_metallic_material(color, name=name, roughness=roughness)

    obj = active_object()
    obj.data.materials.append(material)


def add_lights():
    rig_obj, empty = create_light_rig(light_count=3, light_type="AREA", rig_radius=5.0, energy=150)
    rig_obj.location.z = 3

    bpy.ops.object.light_add(type="AREA", radius=5, location=(0, 0, 5))


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


################################################################
# helper functions END
################################################################


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


def animate_object_update(context, obj, current_frame):
    obj.keyframe_insert("scale", frame=current_frame)
    obj.keyframe_insert("location", frame=current_frame)
    obj.keyframe_insert("rotation_euler", frame=current_frame)

    update_object(obj)

    frame = current_frame + context["frame_count_loop"]

    obj.keyframe_insert("scale", frame=frame)
    obj.keyframe_insert("location", frame=frame)
    obj.keyframe_insert("rotation_euler", frame=frame)

    set_fcurve_interpolation_to_linear()


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


def create_background(color):
    bottom_surface = make_surface(color)
    bottom_surface.location.z -= 0.001

    top_surface = make_surface(color)
    update_object(top_surface)
    top_surface.location.z += 0.001

    bpy.ops.mesh.primitive_plane_add(size=100, location=(0, 0, 0.5))


def main():
    """
    Python code to generate this animation
    https://www.artstation.com/artwork/nEw0mK
    """
    context = scene_setup()

    enable_extra_meshes()
    enable_mod_tools()

    color = get_random_color()
    create_centerpiece(context, color)
    create_background(color)
    add_lights()


if __name__ == "__main__":
    main()

import math
import random
import time

import bpy
import mathutils

################################################################
# helper functions BEGIN
################################################################


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


def add_ctrl_empty(name=None):
    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

    return empty


def setup_camera(loc, rot, frame_count):
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

    camera.data.dof.use_dof = True
    camera.data.dof.focus_object = empty
    camera.data.dof.aperture_fstop = 0.35

    start_value = camera.data.lens
    mid_value = camera.data.lens - 10
    loop_param(camera.data, "lens", start_value, mid_value, frame_count)

    return empty


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

    scene.eevee.use_bloom = True
    scene.eevee.bloom_intensity = 0.005

    # set Ambient Occlusion properties
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 4
    scene.eevee.gtao_factor = 5

    scene.eevee.taa_render_samples = 64

    if bpy.app.version < (4, 0, 0):
        scene.view_settings.look = "Very High Contrast"
    else:
        scene.view_settings.look = "AgX - Very High Contrast"

    set_1080px_square_render_res()


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


def make_fcurves_linear():
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


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


def render_loop():
    bpy.ops.render.render(animation=True)


def apply_random_color_material(obj):
    color = get_random_color()
    mat = bpy.data.materials.new(name="Material")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color

    if bpy.app.version < (4, 0, 0):
        mat.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 0
    else:
        mat.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0

    obj.data.materials.append(mat)


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


################################################################
# helper functions END
################################################################


def animate_shape(obj, vertices, start_frame, end_frame):
    obj.keyframe_insert("rotation_euler", frame=start_frame)

    one_turn = 360 / vertices
    obj.rotation_euler.z += math.radians(one_turn * 2)

    obj.keyframe_insert("rotation_euler", frame=end_frame)

    set_keyframe_to_ease_in_out(obj)


def create_shape(vertices, radius, rotation, location):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=0.1)

    obj = active_object()
    obj.rotation_euler = rotation
    obj.location = location

    apply_random_color_material(obj)

    bpy.ops.object.modifier_add(type="BEVEL")
    obj.modifiers["Bevel"].width = 0.02

    return obj


def gen_centerpiece(context):
    radius_step = 0.1
    radius = 1

    vertices = 5

    shape_count = 100

    z_location_step = -0.1
    current_location = mathutils.Vector((0, 0, 0))

    z_rotation_step = math.radians(5)
    current_rotation = mathutils.Euler((0.0, 0.0, 0.0))

    start_frame_step = 5
    end_frame = context["frame_count"] - 10

    for i in range(shape_count):
        start_frame = start_frame_step * i

        current_rotation.z = z_rotation_step * i
        current_location.z = z_location_step * i

        shape_obj = create_shape(vertices, radius, current_rotation, current_location)
        animate_shape(shape_obj, vertices, start_frame, end_frame)

        radius += radius_step


def main():
    """
    Python code to generate an animation loop
    """
    context = setup_scene()
    gen_centerpiece(context)
    add_lights()


if __name__ == "__main__":
    main()

import random
import time

import addon_utils
import bpy

################################################################
# helper functions BEGIN
################################################################


def purge_orphans():
    """
    Remove all orphan data blocks

    see this from more info:
    https://youtu.be/3rNqVPtbhzc?t=149
    """
    if bpy.app.version >= (3, 0, 0):
        # run this only for Blender versions 3.0 and higher
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True, do_linked_ids=True, do_recursive=True
        )
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


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

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
    camera.data.lens = 45

    camera.data.passepartout_alpha = 0.9

    empty = track_empty(camera)


def set_1k_square_render_res():
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
        world.node_tree.nodes["Background"].inputs[0].default_value = (0.0, 0.0, 0.0, 1)

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

    set_1k_square_render_res()


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


def enable_import_images_as_planes():

    loaded_default, loaded_state = addon_utils.check("io_import_images_as_planes")
    if not loaded_state:
        addon_utils.enable("io_import_images_as_planes")


def add_light():
    bpy.ops.object.light_add(type="SUN")
    sun = active_object()
    sun.data.energy = 2
    sun.data.specular_factor = 0
    sun.data.use_shadow = False


################################################################
# helper functions END
################################################################


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


def get_grid_step(path):
    bpy.ops.import_image.to_plane(files=[{"name": path}])
    plane = active_object()
    x_step = plane.dimensions.x
    y_step = plane.dimensions.y

    bpy.ops.object.delete()

    return x_step, y_step


def gen_centerpiece():
    list_of_video_paths = get_list_of_loops()

    random.shuffle(list_of_video_paths)

    x_step, y_step = get_grid_step(list_of_video_paths[0])

    start_x = -1.5
    stop_x = 2
    current_x = start_x

    current_y = -1.5

    for mp4_path in list_of_video_paths:
        bpy.ops.import_image.to_plane(files=[{"name": mp4_path}])
        obj = active_object()
        obj.location.x = current_x
        obj.location.y = current_y

        shader_nodes = obj.active_material.node_tree.nodes
        shader_nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.0
        shader_nodes["Image Texture"].image_user.use_cyclic = True

        current_x += x_step

        if current_x > stop_x:
            current_x = start_x
            current_y += y_step


def main():
    """
    Python code to generate a grid of loop animations from mp4 files

    Tutorial: https://www.youtube.com/watch?v=1toJeVNOdnk
    """
    setup_scene()
    enable_import_images_as_planes()
    gen_centerpiece()
    add_light()


if __name__ == "__main__":
    main()

import math
import random
import time

import addon_utils
import bpy
import mathutils

################################################################
# helper functions BEGIN
################################################################


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


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def apply_material(material):
    obj = active_object()
    obj.data.materials.append(material)


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

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


def create_detail_rotation(obj, frame_count, x_degrees, y_degrees, z_degrees):
    rotation = obj.rotation_euler

    mid_value = mathutils.Euler(
        (
            rotation.x + math.radians(x_degrees),
            rotation.y + math.radians(y_degrees),
            rotation.z + math.radians(z_degrees),
        ),
        "XYZ",
    )

    obj.keyframe_insert("rotation_euler", frame=1)
    obj.keyframe_insert("rotation_euler", frame=frame_count)

    obj.rotation_euler = mid_value
    obj.keyframe_insert("rotation_euler", frame=frame_count / 2)


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

    scene.eevee.use_bloom = True
    scene.eevee.bloom_intensity = 0.005

    # set Ambient Occlusion properties
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 4
    scene.eevee.gtao_factor = 5

    scene.eevee.taa_render_samples = 64

    scene.view_settings.look = "Very High Contrast"

    set_1080px_square_render_res()

    cycles = True
    if cycles:
        bpy.context.scene.render.engine = "CYCLES"
        bpy.context.scene.cycles.device = "GPU"
        bpy.context.scene.cycles.samples = 1024


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


def make_spline_fcurve_interpolation_linear():
    for fcurve in bpy.context.active_object.data.animation_data.action.fcurves:
        for points in fcurve.keyframe_points:
            points.interpolation = "LINEAR"


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


def render_loop():
    bpy.ops.render.render(animation=True)


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


def create_metal_material():
    color = get_random_color()
    material = bpy.data.materials.new(name="metal_material")
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    material.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
    return material


def apply_hdri(path_to_image, bg_color, hdri_light_strength, bg_strength):
    """
    Based on a technique from a FlippedNormals tutorial
    https://www.youtube.com/watch?v=dbAWTNCJVEs
    """
    world_node_tree = bpy.context.scene.world.node_tree

    nodes_to_remove = []
    for node in world_node_tree.nodes:
        nodes_to_remove.append(node)

    for node in nodes_to_remove:
        world_node_tree.nodes.remove(node)

    location_x = 0
    texture_coordinate_node = world_node_tree.nodes.new(type="ShaderNodeTexCoord")
    texture_coordinate_node.name = "Texture Coordinate"
    texture_coordinate_node.location.x = location_x
    location_x += 200

    mapping_node = world_node_tree.nodes.new(type="ShaderNodeMapping")
    mapping_node.location.x = location_x
    location_x += 200
    mapping_node.name = "Mapping"

    environment_texture_node = world_node_tree.nodes.new(type="ShaderNodeTexEnvironment")
    environment_texture_node.location.x = location_x
    location_x += 300
    environment_texture_node.name = "Environment Texture"
    environment_texture_node.image = bpy.data.images.load(path_to_image)

    background_node = world_node_tree.nodes.new(type="ShaderNodeBackground")
    background_node.location.x = location_x
    background_node.name = "Background"
    background_node.inputs["Strength"].default_value = hdri_light_strength

    background_node_2 = world_node_tree.nodes.new(type="ShaderNodeBackground")
    background_node_2.location.x = location_x
    background_node_2.location.y = -100
    background_node_2.name = "Background.001"
    background_node_2.inputs["Color"].default_value = bg_color
    background_node_2.inputs["Strength"].default_value = bg_strength

    light_path_node = world_node_tree.nodes.new(type="ShaderNodeLightPath")
    light_path_node.location.x = location_x
    light_path_node.location.y = 400
    location_x += 200
    light_path_node.name = "Light Path"

    mix_shader_node = world_node_tree.nodes.new(type="ShaderNodeMixShader")
    mix_shader_node.location.x = location_x
    location_x += 200
    mix_shader_node.name = "Mix Shader"

    world_output_node = world_node_tree.nodes.new(type="ShaderNodeOutputWorld")
    world_output_node.location.x = location_x
    location_x += 200

    # links begin
    from_node = background_node
    to_node = mix_shader_node
    world_node_tree.links.new(from_node.outputs["Background"], to_node.inputs["Shader"])

    from_node = mapping_node
    to_node = environment_texture_node
    world_node_tree.links.new(from_node.outputs["Vector"], to_node.inputs["Vector"])

    from_node = texture_coordinate_node
    to_node = mapping_node
    world_node_tree.links.new(from_node.outputs["Generated"], to_node.inputs["Vector"])

    from_node = environment_texture_node
    to_node = background_node
    world_node_tree.links.new(from_node.outputs["Color"], to_node.inputs["Color"])

    from_node = background_node_2
    to_node = mix_shader_node
    world_node_tree.links.new(from_node.outputs["Background"], to_node.inputs[2])

    from_node = light_path_node
    to_node = mix_shader_node
    world_node_tree.links.new(from_node.outputs["Is Camera Ray"], to_node.inputs["Fac"])

    from_node = mix_shader_node
    to_node = world_output_node
    world_node_tree.links.new(from_node.outputs["Shader"], to_node.inputs["Surface"])
    # links end

    return world_node_tree


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


################################################################
# helper functions END
################################################################


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


def create_emissive_curve():
    emissive_curve = create_base_curve()
    
    emissive_material = create_emissive_material()
    apply_material(emissive_material)
    
    emissive_curve.data.bevel_depth = 0.01


def create_centerpiece(context):
    profile_curve = create_profile_curve()
    
    primary_curve = create_primary_curve(profile_curve)
    animate_point_tilt(primary_curve, context["frame_count"])
    
    create_emissive_curve()


def main():
    """
    Python code to generate this animation
    https://www.artstation.com/artwork/QrOv4E
    """
    context = setup_scene()
    add_lights()
    enable_extra_curves()
    create_centerpiece(context)


if __name__ == "__main__":
    main()

import json
import math
import os
import random
import time

import bpy

################################################################
# helper functions BEGIN
################################################################


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


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    """
    create an empty and add a 'Track To' constraint
    """
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

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

    scene.eevee.use_bloom = True
    scene.eevee.bloom_intensity = 0.005

    # set Ambient Occlusion properties
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 4
    scene.eevee.gtao_factor = 5

    scene.eevee.taa_render_samples = 64

    scene.view_settings.look = "Very High Contrast"

    set_1080px_square_render_res()


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


################################################################
# helper functions END
################################################################


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


def parent_to_empty(text_obj, plane_obj, name):
    empty_obj = add_ctrl_empty(name)
    text_obj.parent = empty_obj
    plane_obj.parent = empty_obj
    return empty_obj
    

def create_centerpiece(context):

    color_palette = select_random_color_palette(context)

    current_y = 0
    for hex_color in color_palette:
        text_obj = create_text_object(hex_color)
        plane_obj = create_color_plane(hex_color)

        empty_obj = parent_to_empty(text_obj, plane_obj, hex_color)
        empty_obj.location.y = current_y

        current_y += 0.4


def main():
    """
    Python code to generate a scene with 5 planes
    and apply a random 5 color palette to them
    """
    context = setup_scene()
    context["color_palettes"] = load_color_palettes()
    create_centerpiece(context)


if __name__ == "__main__":
    main()

"""
See YouTube tutorial here: https://youtu.be/4xtQsmBof_M
"""
import math
import random

import bpy
import mathutils
from bpybb.hdri import apply_hdri
from bpybb.material import apply_material, make_color_ramp_from_color_list
from bpybb.object import apply_location, track_empty
from bpybb.output import set_1080px_square_render_res
from bpybb.random import time_seed
from bpybb.utils import active_object, clean_scene

################################################################
# helper functions BEGIN
################################################################


def get_random_pallet_color(context):
    return random.choice(context["colors"])


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


# Blender 2.8
# def setup_camera(loc, rot):
#     """
#     create and setup the camera for Blender 2.8
#     """
#     bpy.ops.object.camera_add(rotation=(math.radians(90), 0 , 0))
#     camera = active_object()

#     empty_cam = add_ctrl_empty(name=f"empty.cam")
#     empty_cam.location = loc
#     empty_cam.rotation_euler = rot
#     camera.parent = empty_cam

#     # set the camera as the "active camera" in the scene
#     bpy.context.scene.camera = camera

#     # set the Focal Length of the camera
#     camera.data.lens = 70

#     camera.data.passepartout_alpha = 0.9

#     empty = track_empty(empty_cam)

#     return empty


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
        world.node_tree.nodes["Background"].inputs[0].default_value = (0.0, 0.0, 0.0, 1)

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


def get_color_palette():
    # https://www.colourlovers.com/palette/2943292
    # palette = ['#D7CEA3FF', '#907826FF', '#A46719FF', '#CE3F0EFF', '#1A0C47FF']

    palette = [
        [0.83984375, 0.8046875, 0.63671875, 1.0],
        [0.5625, 0.46875, 0.1484375, 1.0],
        [0.640625, 0.40234375, 0.09765625, 1.0],
        [0.8046875, 0.24609375, 0.0546875, 1.0],
        [0.1015625, 0.046875, 0.27734375, 1.0],
    ]

    return palette


def setup_scene():
    fps = 30
    loop_seconds = 6
    frame_count = fps * loop_seconds

    project_name = "color_slices"
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

    loc = (-8, -6, 7.5)
    rot = (0, 0, 0)
    cam_empty = setup_camera(loc, rot)
    cam_empty.location.z = 4.5

    context = {
        "frame_count": frame_count,
    }

    context["colors"] = get_color_palette()

    return context


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


################################################################
# helper functions END
################################################################


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


def gen_scene(context):
    gen_centerpiece(context)
    add_lights(context)


def gen_centerpiece(context):

    random_location = mathutils.Vector((random.uniform(0, 100), random.uniform(0, 100), random.uniform(0, 100)))

    curve_count = 100
    context["material"] = setup_material(context)
    context["bevel object"] = create_bevel_object()
    context["radius"] = 1.1
    start_frame = 1
    for i in range(curve_count):
        current_z = 0.1 * i
        shape_key = gen_perlin_curve(context, random_location, current_z)

        start_frame = animate_curve(shape_key, start_frame)


def main():
    """
    Python code for this art project
    https://www.artstation.com/artwork/48wX6L

    Tutorial Video about this script:
    https://www.youtube.com/watch?v=4xtQsmBof_M&list=PLB8-FQgROBmlzQ7Xkq4YU7u08Zh3iuyPD&index=9
    """
    context = setup_scene()

    gen_scene(context)


if __name__ == "__main__":
    main()

