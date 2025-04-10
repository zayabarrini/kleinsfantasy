import bpy
import random
from mathutils import Vector
import traceback

def apply_icing_with_sprinkles(target_object, icing_thickness=0.025, sprinkle_count=300):
    """
    Applies realistic icing and sprinkles to any object, following Blender Guru's donut techniques.
    
    Args:
        target_object (bpy.types.Object): The object to decorate
        icing_thickness (float): Thickness of the icing layer in meters
        sprinkle_count (int): Number of sprinkles to add
    """
    try:
        # Ensure we're in Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = target_object
        
        print(f"Creating icing for {target_object.name}...")
        
        # Duplicate the object for icing
        bpy.ops.object.select_all(action='DESELECT')
        target_object.select_set(True)
        bpy.ops.object.duplicate()
        icing = bpy.context.active_object
        icing.name = f"{target_object.name}_Icing"
        
        # Add solidify modifier for thickness
        solidify = icing.modifiers.new(name="Icing_Thickness", type='SOLIDIFY')
        solidify.thickness = icing_thickness
        solidify.offset = 1.0  # Push outward
        solidify.use_rim = True
        solidify.edge_crease_inner = 1.0  # Makes icing hug the surface
        
        # Subdivide for detail
        subdiv = icing.modifiers.new(name="Subdivision", type='SUBSURF')
        subdiv.levels = 2
        subdiv.render_levels = 2
        
        # Apply modifiers to make geometry editable
        bpy.ops.object.modifier_apply(modifier=solidify.name)
        bpy.ops.object.modifier_apply(modifier=subdiv.name)
        
        # Enter Edit Mode to shape the icing
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Create natural edge with proportional editing
        bpy.context.scene.tool_settings.proportional_edit = 'ENABLED'
        bpy.context.scene.tool_settings.proportional_edit_falloff = 'SMOOTH'
        bpy.context.scene.tool_settings.proportional_size = 0.1
        
        # Randomly adjust edge vertices
        bpy.ops.transform.translate(
            value=(0, 0, random.uniform(-0.01, 0.01)),
            proportional_size=0.1,
            snap=True,
            snap_target='FACE'
        )
        
        # Create dribbles
        for _ in range(random.randint(3, 6)):
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Select random edge vertex
            verts = [v for v in icing.data.vertices if v.co.z > 0]
            if verts:
                v = random.choice(verts)
                v.select = True
                bpy.ops.object.mode_set(mode='EDIT')
                
                # Extrude downward
                bpy.ops.mesh.extrude_vertices_move(
                    TRANSFORM_OT_translate={
                        "value": (0, 0, random.uniform(-0.03, -0.01)),
                        "snap": True,
                        "snap_target": 'FACE'
                    }
                )
        
        # Return to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Add material to icing
        if "Icing_Material" not in bpy.data.materials:
            mat = bpy.data.materials.new(name="Icing_Material")
            mat.diffuse_color = (0.9, 0.9, 1.0, 1.0)
            mat.specular_intensity = 0.5
            mat.subsurface_scattering.radius = (1.0, 0.5, 0.1)
        icing.data.materials.append(bpy.data.materials["Icing_Material"])
        
        print("Adding sprinkles...")
        # Create sprinkle collection
        if "Sprinkles" not in bpy.data.collections:
            sprinkle_collection = bpy.data.collections.new("Sprinkles")
            bpy.context.scene.collection.children.link(sprinkle_collection)
        else:
            sprinkle_collection = bpy.data.collections["Sprinkles"]
        
        # Create sprinkle object (cylinder)
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.01, depth=0.1)
        sprinkle_base = bpy.context.active_object
        sprinkle_base.name = "Sprinkle_Base"
        sprinkle_base.hide_viewport = True
        sprinkle_base.hide_render = True
        
        # Create sprinkles
        for i in range(sprinkle_count):
            sprinkle = sprinkle_base.copy()
            sprinkle.data = sprinkle_base.data.copy()
            sprinkle.name = f"Sprinkle_{i:03d}"
            
            # Random position on icing surface
            sprinkle.location = icing.location + Vector((
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(-0.5, 0.5)
            ))
            
            # Random rotation and scale
            sprinkle.rotation_euler = (
                random.uniform(0, 3.14159),
                random.uniform(0, 3.14159),
                random.uniform(0, 3.14159)
            )
            scale_factor = random.uniform(0.8, 1.2)
            sprinkle.scale = (scale_factor*0.5, scale_factor*0.5, scale_factor)
            
            # Random color
            mat = bpy.data.materials.new(name=f"Sprinkle_Mat_{i}")
            mat.diffuse_color = (
                random.uniform(0.2, 1.0),
                random.uniform(0.2, 1.0),
                random.uniform(0.2, 1.0),
                1.0
            )
            sprinkle.data.materials.append(mat)
            
            sprinkle_collection.objects.link(sprinkle)
        
        print(f"Successfully added icing with {sprinkle_count} sprinkles to {target_object.name}!")
        return icing
        
    except Exception as e:
        print("Error applying icing:", e)
        traceback.print_exc()
        return None

# Modified create_klein_bottle with icing option
def create_klein_bottle(add_icing=True):
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
                # print(f"Klein bottle created: {klein_bottle}")
                if klein_bottle and add_icing:
                    apply_icing_with_sprinkles(klein_bottle)
                return klein_bottle

       
    except Exception as e:
        print("Error creating the Klein bottle:", e)
        traceback.print_exc()
        return None


# Example usage:
if __name__ == "__main__":
    klein = create_klein_bottle(add_icing=True)
    if klein:
        print(f"Successfully created decorated Klein bottle: {klein.name}")