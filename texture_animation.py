import bpy
import traceback

def create_texture_material(klein_bottle):
    """Create a material with two textures that can be animated."""
    try:
        # Create a new material and enable nodes
        material = bpy.data.materials.new(name="AnimatedTextureMaterial")
        material.use_nodes = True
        node_tree = material.node_tree
        print("Material with nodes created.")

        # Add the material to the Klein bottle object
        klein_bottle.data.materials.append(material)
        print(f"Material applied to {klein_bottle.name}.")

        # Access the node tree and remove default nodes
        nodes = node_tree.nodes
        nodes.clear()
        print("Cleared default nodes from the material.")

        # Add Principled BSDF
        bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        bsdf.location = (0, 0)

        # Add Texture 1 (Image Texture 1)
        tex_image1 = nodes.new(type="ShaderNodeTexImage")
        tex_image1.image = bpy.data.images.load("/path/to/texture1.png")  # Replace with actual path
        tex_image1.location = (-300, 200)
        print("Texture 1 node created and image loaded.")

        # Add Texture 2 (Image Texture 2)
        tex_image2 = nodes.new(type="ShaderNodeTexImage")
        tex_image2.image = bpy.data.images.load("/path/to/texture2.png")  # Replace with actual path
        tex_image2.location = (-300, -200)
        print("Texture 2 node created and image loaded.")

        # Add Mix Shader to blend between the textures
        mix_shader = nodes.new(type="ShaderNodeMixShader")
        mix_shader.location = (200, 0)
        print("Mix Shader node created.")

        # Add an RGB input to control the texture blending
        mix_input = nodes.new(type="ShaderNodeRGB")
        mix_input.location = (-150, 0)
        print("RGB input node created to control texture blending.")

        # Connect nodes
        links = node_tree.links
        links.new(tex_image1.outputs["Color"], bsdf.inputs["Base Color"])
        links.new(tex_image2.outputs["Color"], bsdf.inputs["Base Color"])
        links.new(mix_input.outputs["Color"], mix_shader.inputs[0])
        print("Nodes connected for texture blending.")

        return material, mix_input
    except Exception as e:
        print("Error creating texture material:", e)
        traceback.print_exc()
        return None, None

def animate_texture_transition(mix_input):
    """Animate the transition between two textures using the mix input color."""
    try:
        # Set initial color (fully texture 1)
        mix_input.outputs["Color"].default_value = (1, 0, 0, 1)
        mix_input.keyframe_insert(data_path="default_value", frame=1)
        print("Keyframe set for texture 1 at frame 1.")

        # Set final color (fully texture 2)
        mix_input.outputs["Color"].default_value = (0, 1, 0, 1)
        mix_input.keyframe_insert(data_path="default_value", frame=50)
        print("Keyframe set for texture 2 at frame 50.")

    except Exception as e:
        print("Error animating texture transition:", e)
        traceback.print_exc()

def main():
    print("Starting texture animation setup for Klein bottle...")
    clear_scene()

    # Create Klein bottle and material
    klein_bottle = create_klein_bottle()
    if klein_bottle:
        material, mix_input = create_texture_material(klein_bottle)
        
        # Ensure material and input exist before animation
        if material and mix_input:
            animate_texture_transition(mix_input)
            print("Texture animation setup complete.")
        else:
            print("Failed to create material or mix input for animation.")
    else:
        print("Failed to create Klein bottle; exiting script.")

# Run the script
main()

