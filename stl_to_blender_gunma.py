import os
import bpy
from pathlib import Path
from stat import ST_SIZE

# input parent dir path
dir_path = str(r"I:\20220923_Gunma_Kimura_WhaleDataBase")

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

# make set of specimen numbers
list_spnum = list()

for i in range(len(list_stl)):
    list_spnum.append(str(list_stl[i]).split("_")[-1]) # listing spnum like a "GMNH-VM-474.stl"
    
set_spnum = set(list_spnum)

# import stl files with spnum
for i in set_spnum: 
    basename = str() # name for Title and Blender file name
    for stl in list_stl:
        spname = str(stl).split("_")
        if spname[-1] == i:
            basename = spname[-4] + "_" + spname[-3] + "_" + spname[-1].split(".")[0]
            importpath = str(stl)
            # import stl
            bpy.ops.import_mesh.stl(filepath=importpath, 
                                     axis_forward='-Z', 
                                     axis_up='Y', 
                                     filter_glob="*.stl")
            
            # geometry to origin
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
            bpy.ops.object.location_clear(clear_delta=False)
            dim_x = bpy.context.object.dimensions.x
            
            # pe or tyb
            if str(stl).split("_")[-2] == "pe":
                translate((dim_x,0,0))
            
            elif str(stl).split("_")[-2] == "tyb":
                translate((-(dim_x),0,0))
                
            else:
                print("There is unknown part. Please named pe or tyb.") # Unknown object
                break

        else:
            continue

    #   add sphere at origin
    bpy.ops.mesh.primitive_uv_sphere_add(radius=(5))

    #   save blender file with specimen number
    save_blender(dir_path, basename)
    
    # Sketchfab upload
    bpy.data.window_managers["WinMan"].sketchfab_export.title = basename
    bpy.ops.wm.sketchfab_export()

    delete_whole_models()
