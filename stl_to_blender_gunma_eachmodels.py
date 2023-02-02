import os
import bpy
from pathlib import Path
from stat import ST_SIZE

# input parent dir path
dir_path = str(r"I:\20220923_Gunma_Kimura_WhaleDataBase\periotic_tympanic_bulla_for_upload\models")

# get whole file names specimen number
def search_stl(path,list_stl):
    """
    output list of dir of stl under the folder.
    """
    p = Path(path)
    i = 0
    for file in p.iterdir():
        if file.is_dir():
            search_stl(file,list_stl)
        elif file.is_file():
            base, ext = os.path.splitext(file) #make taple
            if ext == ".stl":
                # resolve()を使って絶対パスを表示する
                list_stl.append(file.resolve())
    return list_stl

# move model
def translate(vector):
        bpy.ops.transform.translate(value=vector, constraint_axis=(True,True,True))
        
# del whole models
def delete_whole_models():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

# save blender file
def save_blender(path, specimen_name):
    p = Path(path + "\\" + specimen_name + ".blend")
    bpy.ops.wm.save_as_mainfile(filepath = str(p))

# add material from https://blender.stackexchange.com/questions/153094/blender-2-8-python-how-to-set-material-color-using-hex-value-instead-of-rgb
def add_material(obj, material_name, r, g, b):
    material = bpy.data.materials.get(material_name)
    if material is None:
        material = bpy.data.materials.new(material_name)
    material.use_nodes = True
    principled_bsdf = material.node_tree.nodes['Principled BSDF']
    if principled_bsdf is not None:
        principled_bsdf.inputs[0].default_value = (r, g, b, 1)  
    obj.active_material = material

# make list whole stl path
list_stl = search_stl(dir_path,[])
# print(list_stl)

basename = str() # name for Title and Blender file name
for stl in list_stl:
    filename = str(stl).split("\\")
    # print(spname)
    basename = filename[-1].split(".")[0] # like a "Ziphius_cavirostris_USNM530291_tyb"
    # print("basename is " + basename)
    importpath = str(stl)
    # print(importpath)

    # import stl
    bpy.ops.import_mesh.stl(filepath=importpath, 
                                axis_forward='-Z', 
                                axis_up='Y', 
                                filter_glob="*.stl")
    
    # geometry to origin 
    obj = bpy.ops.object 
    obj.origin_set(type='GEOMETRY_ORIGIN')
    obj.location_clear(clear_delta=False)
    dim_x = bpy.context.object.dimensions.x

    obj_act = bpy.context.active_object
    material_name = 'gray'
    add_material(obj_act, material_name, 0.44,0.44,0.44)
    #add_material(obj_act, material_name, 0.8,0,0)
        
    # add sphere at origin and move with x axis
    sphere = bpy.ops.mesh.primitive_uv_sphere_add(radius=(5))
    translate((dim_x,0,0))
    obj_act = bpy.context.active_object
    add_material(obj_act, material_name, 0.44,0.44,0.44)
    #add_material(obj_act, material_name, 0.8,0,0)

    # save blender file with STL file name
    save_blender(dir_path, basename)

    # Sketchfab upload
    # bpy.data.window_managers["WinMan"].sketchfab_export.title = basename
    # bpy.ops.wm.sketchfab_export()

    delete_whole_models()
