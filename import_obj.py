import os
import bpy
from pathlib import Path
from stat import ST_SIZE

# input parent dir path
dir_path = str(r"I:\20220902_Kahaku_Whales")

# get whole layer collection https://bookyakuno.com/get-all-view-layer-collection/
def get_all_vl_colle(tgt_colle, all_l):
    for i in tgt_colle:
        for c in i.children:
            all_l += [c]
            get_all_vl_colle(c.children, all_l)
    return set(all_l)

def search_obj(path,list_obj): # recursive function
    """
    output list of dir of obj under the folder.
    """
    p = Path(path)
    i = 0
    for file in p.iterdir():
        if file.is_dir():
            search_obj(file,list_obj)
        elif file.is_file():
            base, ext = os.path.splitext(file) #make taple
            if ext == ".obj":
                # resolve()を使って絶対パスを表示する
                list_obj.append(file.resolve())
    return list_obj

def new_collection(name):
    collection = bpy.context.blend_data.collections.new(name = name)
    bpy.context.collection.children.link(collection)
    
def actv_collection(n):
    viewlayer = bpy.context.view_layer
    all_layer = viewlayer.layer_collection.children.values()
    get_all_vl_colle(all_layer, all_layer)
    viewlayer.active_layer_collection = all_layer[n]

list_obj = search_obj(dir_path,[])

new_collection("IMPORTED") # Make Top collection

actv_collection(0) # Activate Top collection

for i in list_obj:
    importpath = str(i)
    basename = os.path.splitext(os.path.basename(importpath))[0]

    # Make new collection
    new_collection(basename)

    # activate the latest collection
    actv_collection(-1)
    
    # import obj
    bpy.ops.import_scene.obj(filepath=importpath, 
                             axis_forward='-Z', 
                             axis_up='Y', 
                             filter_glob="*.obj;*.mtl", 
                             use_edges=True, 
                             use_smooth_groups=True, 
                             use_split_objects=True, 
                             use_split_groups=True, 
                             use_groups_as_vgroups=False, 
                             use_image_search=True, 
                             split_mode='ON', 
                             global_clamp_size=0.0)
    
    # Activate Top collection                         
    actv_collection(0)