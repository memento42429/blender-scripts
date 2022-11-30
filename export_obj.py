import os
import bpy

"""
export_obj.py Kent Mori 2022
Export whole selected models each collection each models. 
This script makes new folder with the collection name under the path where exist the blender file.
You can choose export format whithin obj or stl. 
This script works on Windows OS. 
"""

fileFormat = "obj" # select obj or stl

def modelExport(fileFormat = "obj"):

    selected = bpy.context.selected_objects

    for model in selected:
        bpy.ops.object.select_all(action='DESELECT')    # at first, deselect all
        model.select_set(True)  # select one object for export
        modelname = model.name # the name of model ex) 13_029_001_KaruGamo_10K
        collname = model.users_collection[0].name
        # print(collname)
        # print(type(collname))
        
        basename = '_'.join(collname.split('_',3)[:3]) + '_models'
        # print(basename)
        
        dir = bpy.path.abspath(r"//" + basename + "\\fromBlender")
        if not os.path.exists(dir):
            os.makedirs(dir)
        # print(dir)
        
        
        
        if fileFormat == "obj":
            exportPath = dir + "\\" + modelname + ".obj"
            # print(exportPath)
            bpy.ops.export_scene.obj(filepath=exportPath, 
            check_existing=True, 
            filter_glob='*.obj;*.mtl', 
            use_selection=True,    # checked
            use_animation=False, 
            use_mesh_modifiers=True, 
            use_edges=True, 
            use_smooth_groups=False, 
            use_smooth_groups_bitflags=False, 
            use_normals=True, 
            use_uvs=True, 
            use_materials=True, 
            use_triangles=False, 
            use_nurbs=False, 
            use_vertex_groups=False, 
            use_blen_objects=True, 
            group_by_object=False, 
            group_by_material=False, 
            keep_vertex_order=False, 
            global_scale=1.0, 
            path_mode='AUTO', 
            axis_forward='-Z', 
            axis_up='Y')

        elif fileFormat == "stl":
            exportPath = dir + "\\" + modelname + ".stl"
            # print(exportPath)
            bpy.ops.export_mesh.stl(filepath=exportPath, 
            check_existing=True, 
            filter_glob='*.stl', 
            use_selection=True,     # checked
            global_scale=1.0, 
            use_scene_unit=False, 
            ascii=False, 
            use_mesh_modifiers=True, 
            batch_mode='OFF', 
            # global_space=((0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0)), 
            axis_forward='Y', 
            axis_up='Z')

        else:
            print("please select obj or stl")
            break

        print(modelname + "exported with" + fileFormat)
    print("export finished")

modelExport(fileFormat)