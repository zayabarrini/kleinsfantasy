Here's a concise summary of your Blender donut tutorial notebook:

---

### **Blender Donut Tutorial Notes**  
*Based on Blender Guru's [Beginner Tutorial Series](https://www.youtube.com/watch?v=TPrnSACiTJ4&list=PLjEaoINr3zgEq0u2MzVgAaHEBt--xLB6U).*  

#### **Setup**  
- Blender 2.92 (tutorial uses 2.8).  
- Recommended: Mouse with scroll wheel (MMB), NumPad, and shortcut familiarity.  
- Key abbreviations: LMB (left), MMB (middle), RMB (right).  

#### **Basics (Part 1)**  
- **Transformations**:  
  - Move (`G`), Scale (`S`), Rotate (`R`).  
  - Lock to axis: `X/Y/Z` or `MMB` (press before moving).  
  - Enter values: e.g., `R → 180 → Enter` for 180° rotation.  
- **View Navigation**:  
  - Orbit (`MMB`), Pan (`Shift+MMB`), Zoom (scroll wheel).  
- **Misc**:  
  - Focus on object: `NumPad .`  
  - Add/delete objects: `Shift+A`, `Del`.  

#### **Modeling (Part 2)**  
1. **Donut Shape**:  
   - Add torus, adjust segments (28 major, 12 minor).  
   - Edit Mode (`Tab`), enable *Proportional Editing* (radius ~0.06).  
   - Sculpt by dragging vertices.  
2. **Smoothing**:  
   - *Shade Smooth* + *Subdivision Surface* modifier.  

#### **Icing (Part 3)**  
1. **Separate Icing**:  
   - X-ray mode (`Alt+Z`), select top vertices, duplicate (`Shift+D`), separate (`P`).  
   - Rename: "Donut" (base), "Icing" (top).  
2. **Thicken Icing**:  
   - Add *Solidify* modifier (thickness: 2.5mm, offset: 1).  
   - Reorder modifiers (*Solidify* above *Subdivision* for rounded edges).  

#### **Refining Icing (Part 4)**  
1. **Subdivide**:  
   - Edit Mode, select all (`A`), subdivide (smoothness: 1).  
2. **Drips**:  
   - Select edge loop (`Alt+LMB`), invert (`Ctrl+I`), hide (`H`).  
   - Enable *Snap* (Face + Project Individual Elements).  
   - Drag edge vertices with *Proportional Editing* (Sharp falloff) for natural drips.  

---

**Visual Guide**: See [`journey.md`](journey.md) for a quick summary.  

*Notes include troubleshooting tips and clarifications from the tutorial.*


---

### **Level 1, Part 4 (Continued) – Icing Dribbles**  
- **Extrude dribbles**:  
  - Enable *Proportional Editing* (Smooth), select edge vertices, extrude (`E`).  
  - Fix jaggedness: Increase *Subdivision* modifier *Levels Viewport* to 2.  
- **Snap to surface**:  
  - Enable *Face* snapping + *Project Individual Elements* to align dribbles with donut.  
  - Adjust *Crease Inner* (Solidify modifier) to 1 for tighter icing contact.  

### **Level 1, Part 5 – Sculpting Details**  
1. **Backup**: Duplicate donut/icing (`Shift+D`), move to "Archive" collection (hide via eye icon).  
2. **Subdivision**:  
   - Apply *Subdivision* modifier (*Levels Viewport: 2* for donut, *3* for icing) to increase mesh density.  
3. **Sculpting**:  
   - Use *Inflate* brush to thicken dribbles, *Grab* brush for raggedy edges, *Draw* for surface texture.  
   - Fix overhangs: Enable *Proportional Editing*, pull vertices toward donut (`G`/`R`).  

### **Level 1, Part 6 – Rendering**  
1. **Lighting**:  
   - Move light closer, reduce *Power* to 40W. Enable *Contact Shadows* (Eevee) or switch to *Cycles* for realistic shadows.  
   - *Cycles Tip*: Use *GPU Compute* (OptiX/CUDA) for faster renders.  
2. **Camera**:  
   - Align view: Navigate normally, press `Ctrl+Alt+NumPad 0` to match camera.  
   - Refine with *Camera to View* (Side panel `N` > *View* tab).  
3. **Final Render**:  
   - Render (`F12`), save image (`Alt+S`).  
   - For sunlight effect: Move light far away, increase *Power* to 500W.  

---

**Key Shortcuts**:  
- `E`: Extrude | `F12`: Render | `Ctrl+Alt+NumPad 0`: Match camera to view.  
- `Shift+D`: Duplicate | `Ctrl+P`: Parent objects.  

*Notes include troubleshooting for shadows, GPU setup, and camera alignment.*

Here's a concise summary of the materials and rendering section:

---

### **Materials & Rendering**  

#### **1. Basic Materials**  
- **Plane**:  
  - Add material (HSV: 0.6, 0.8, 0.9 for light blue).  
  - Color affects scene lighting (e.g., blue tint on donut).  
- **Icing**:  
  - Key properties:  
    - *Base Color* (HSV: 0.88, 0.35, 0.9 for pink).  
    - *Roughness* (0.34 for slight shine).  
    - *Subsurface* (0.3) + *Subsurface Color* (similar to base) + *Radius* (0.3, 0.15, 0.15).  
- **Donut**:  
  - *Base Color* (HSV: 0.08, 0.44, 0.9).  
  - Minimal *Subsurface* (0.1) for slight light scatter.  

#### **2. Lighting & Rendering**  
- **Soft Shadows**:  
  - Increase light *Size* (0.45m) and reduce *Power* (330W) for softer shadows.  
- **Color Calibration**:  
  - Use *False Color* mode (*Render Properties* > *Color Management*) to check exposure (aim for gray/green zones).  
- **Noise Reduction**:  
  - Enable *Denoising Data* (*Layer Properties*).  
  - In *Compositing* workspace:  
    1. Add *Denoise* node between *Render Layers* and *Composite*.  
    2. Connect: *Noisy Image* → *Image*, *Denoising Normal* → *Normal*, *Denoising Depth* → *Depth*.  
    3. Re-render (`F12`) for clean output.  

#### **3. Workflow Tips**  
- **View Splitting**:  
  - Drag view corners to create splits (e.g., camera + free view).  
- **Overlays**:  
  - Toggle *Show Overlays* (upper-right) to reduce clutter.  
- **Realtime Adjustments**:  
  - Use *Image Editor* to tweak denoising on existing renders.  

---

**Key Shortcuts**:  
- `F12`: Render | `Ctrl+Space`: Maximize view.  
- `Shift+A`: Add node (Compositing).  

*Next: [Level 2](LEVEL-2.md) (texturing, particles, and animation).*

Here's a concise summary of Level 2:

---

### **Blender Donut Tutorial - Level 2 Summary**

#### **1. Particle Systems for Sprinkles**
- **Setup**:
  - Created a basic sprinkle mesh (UV sphere scaled/flattened)
  - Organized objects into collections ("Donut", "Environment", etc.)
- **Particle System**:
  - Added *Hair* particles to icing, rendered as sprinkle objects
  - Adjusted *Scale Randomness* and *Rotation* for natural variation
  - Used *Weight Painting* to control sprinkle placement (avoiding underside)

#### **2. Random Materials**
- **Color Variation**:
  - Used *Object Info* node's *Random* output → *ColorRamp* → *Principled BSDF*
  - Set *Constant* interpolation for distinct sprinkle colors
- **Size Variation**:
  - Created multiple sprinkle shapes (short/long/bent)
  - Rendered particles as a *Collection* for mixed shapes
  - Fixed origin points (*Origin to Geometry*) for proper alignment

#### **3. Final Touches**
- **Intersection Issues**:
  - Blender’s particle system can’t prevent overlapping sprinkles
  - Workaround: Adjust *Seed* value to regenerate placements
- **Optimization**:
  - Reduced *Emission* count (~800 sprinkles)
  - Used *Material Preview* mode for faster previews

---

**Key Workflows**:
- `Ctrl+Tab`: Switch to *Weight Paint* mode  
- `Shift+A`: Add nodes (e.g., *ColorRamp*)  
- `F2`: Rename objects  

*Next: [Level 3](LEVEL-3.md) (texturing, lighting, and final renders).*  

--- 

*Notes cover troubleshooting for particle placement, material nodes, and viewport optimization.*

Here's a concise summary of the texture painting section:

---

### **Texture Painting the Donut**

#### **1. UV Mapping Basics**
- **Issue Detection**:  
  - Painted test patterns revealed UV map problems (texture bleeding/wrapping)
  - Fixed by marking seams and re-unwrapping (see [`uv-unwrapping.md`](uv-unwrapping.md))
- **Key Steps**:  
  - Mark seams with `Ctrl+E` → *Mark Seam*  
  - Unwrap with *Follow Active Quads*  
  - Scale UV map to fit image bounds  

#### **2. Painting Process**
- **Setup**:  
  - Created 2048×1024 texture ("Donut_texture")  
  - Linked via *Image Texture* node to material  
- **Base Layer**:  
  - Filled with donut base color (HSV: 0.08, 0.44, 0.9)  
- **Frosting Belt**:  
  - Used textured brush (*Clouds* mask, *Random* mapping)  
  - White belt (HSV: 0, 0, 1) with 0.3 strength  
  - Painted inner/outer rings  

#### **3. Workflow Tips**
- **Navigation**:  
  - Adjust *Clip Start* (~10cm) to access donut hole  
  - `X` toggles between primary/secondary colors  
- **Brushes**:  
  - Saved custom brushes for base/frosting layers  
  - Disabled *Anti-Aliasing* for better performance  

---

**Key Shortcuts**:  
- `Ctrl+E`: Mark seam | `X`: Swap brush colors  
- `F`: Adjust brush size | `Alt+S`: Save texture  

*Next: [Level 3](LEVEL-3.md) (final textures, lighting, and rendering).*  

--- 

*Notes cover UV troubleshooting and optimized painting techniques.*

Here's a concise summary of the final donut texturing section:

---

### **Final Donut Texturing & Refinements**

#### **1. Procedural Displacement**
- **Node Setup**:
  - Added *Noise Texture* nodes (scale 1500 for fine bumps, 200 for large blisters)
  - Combined via *Add* node (Fac: 0.74)  
  - Used *ColorRamp* to enhance blister definition  
- **Displacement**:
  - Set *Displacement and Bump* in material settings  
  - Adjusted *Scale* to 0.002 for subtlety  

#### **2. Color Variation**
- **Burnt Blisters**:
  - Mixed noise output with base color via *Overlay* blend mode  
  - Darkened blisters (HSV: 0.07, 0.7, 0.65)  
- **Texture Painting**:
  - White frosting belt painted with textured brush  
  - UV fixes applied to prevent seams  

#### **3. Customization Options**
- **Sprinkles**:
  - Adjusted *Scale* and *Number* in particle settings  
  - Weight painting for irregular distribution  
- **Material Tweaks**:
  - Modified *Subsurface* values for icing translucency  
  - Emission effects for "radioactive" look  

#### **4. Node Layout**
![Final node setup](final-node-layout.png)  

---

**Key Adjustments**:  
- `Ctrl+Shift+LMB`: Quick node preview  
- `Alt+Shift+Z`: Toggle overlays for clean renders  

**Example Renders**:  
*Final donut* | *No blister darkening* | *No large bumps*  
![Final](render-final-donut.png) | ![No burn](render-final-donut-no-burn.png) | ![No large](render-final-donut-no-large-lumps.png)  

*Next: [Level 3](LEVEL-3.md) (coffee cup, lighting, and final scene).*  

--- 

*Notes cover displacement scaling, blend modes, and weight painting techniques.*

