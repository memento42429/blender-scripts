import os
import bpy
from pathlib import Path
from stat import ST_SIZE

# input parent dir path
dir_path = str(r"I:\20220923_Gunma_Kimura_WhaleDataBase\periotic_tympanic_bulla_for_upload\test")

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
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
    bpy.ops.object.location_clear(clear_delta=False)
    dim_x = bpy.context.object.dimensions.x
        
    # add sphere at origin and move with x axis
    bpy.ops.mesh.primitive_uv_sphere_add(radius=(5))
    translate((dim_x,0,0))

    # save blender file with STL file name
    save_blender(dir_path, basename)

    # Sketchfab upload
    # bpy.data.window_managers["WinMan"].sketchfab_export.title = basename
    # bpy.ops.wm.sketchfab_export()

    delete_whole_models()
