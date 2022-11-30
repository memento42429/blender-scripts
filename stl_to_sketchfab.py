import os
import bpy
import rojoSKFupload
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
def save_blender(path, sp_name):
    p = Path(path + "\\" + sp_name + ".blend")
    bpy.ops.wm.save_as_mainfile(filepath = str(p))


def skfupload(path, sp_name): # data is csv included specimen infomation
    path = path + "\\" + sp_name + ".blend"
    if model_url := rojoSKFupload.upload(path, name = basename):
        if rojoSKFupload.poll_processing_status(model_url):
            rojoSKFupload.patch_model(model_url)
            rojoSKFupload.patch_model_options(model_url)


# make list whole stl path
list_stl = search_stl(dir_path,[])

# make set of specimen numbers
list_spnum = list()

for i in range(len(list_stl)):
    list_spnum.append(str(list_stl[i]).split("_")[-2]) # listing spnum like a "GMNH-VM-474.stl"
    
set_spnum = set(list_spnum) # set of spnum like a "GMNH-VM-474.stl"

# import stl files with spnum
for i in set_spnum: 
    basename = str() # basename is used for Title and Blender file name
    for stl in list_stl:
        spname = str(stl).split("_") # list
        if spname[-2] == i: # Specimen number "GMNH-VM-474.stl"
            basename = spname[-4] + "_" + spname[-3] + "_" + spname[-2].split(".")[0] # Berardius_bairdii_GMNH-VM-474_pe
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
            if str(stl).split("_")[-1] == "pe":
                translate((dim_x,0,0))
            
            elif str(stl).split("_")[-1] == "tyb":
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
    #skfupload(dir_path, basename) # data is csv included specimen infomation

    #initialize
    delete_whole_models()