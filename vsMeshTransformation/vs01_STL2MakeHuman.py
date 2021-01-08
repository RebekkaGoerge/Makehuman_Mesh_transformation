#  
# This script prepare a mesh to work with makehuman, the mesh can also be modified through the parameters
#
# to run: 
#
# blender --background --python vs01_STL2MakeHuman.py
#
import bpy
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *

import shutil ,os,sys, subprocess, time
from datetime import datetime
from multiprocessing import Process, Pool
from sys import platform


print("========================================================")
print("                    process starts                      ")
print("========================================================")

print(" plugins download and installations ......................")

print("settings paths ......................")
# 
delayTime =20   # time needed to open makehuman

#============================================
#parameters to adapt from user:
#============================================
projectPath     = os.path.join(os.path.expanduser("~"),"Documents","Studium","meshingtools")
#the model name
modelName       = "T3_large"
#the decimation value 
decimate_value  = 0.95
doCompress      = 1  # to disable compression process

exportSTL       = 1 # if true a stl file with modified weight is generated, otherwise only the makehuman proxy is generated 
#the weight in percent
vsWeight        = 1.0

cModelName=modelName+"_s"
outputModelFnm=cModelName + "_mkh"#+time

doMinimize      = 1
doMKWork        = 0
#TODO: automate getting windows paths

mkhPath             = os.path.join(os.path.expanduser("~"),"sw","makehuman-1.2.0.beta2","makehuman","makehuman")
mkh_data            = os.path.join(os.path.expanduser("~"),"Documents","makehuman","v1py3","data")
path_to_model       = os.path.join(projectPath ,"data" )
modelPath           = os.path.join(path_to_model,modelName+".stl")
compressedModelPath = modelPath[:-4]+"_s.stl"

vsScriptSrcPath    = os.path.join(projectPath ,"vsMeshTransformation", "9_vsScript.py")
vsScriptPath       = os.path.join(os.path.expanduser("~"),"Documents","makehuman","v1py3","plugins","9_vsScript.py")
vtkSTLcompressPath = os.path.join(projectPath ,"vsMeshTransformation", "vtkSTLcompress.py")

if platform == "win32":
   mkhPath        = os.path.join('c:', os.sep,"Program Files","makehuman-community")
   path_to_model       = os.path.join(projectPath ,"data" )
   modelPath           = os.path.join(path_to_model,modelName+".stl")
   compressedModelPath = modelPath[:-4]+"_s.stl"
   vsScriptSrcPath    = os.path.join(projectPath ,"vsMeshTransformation", "9_vsScript.py")
   vtkSTLcompressPath = os.path.join(projectPath ,"vsMeshTransformation", "vtkSTLcompress.py")


mkh_source      = os.path.join(mkh_data,"clothes")
mkh_destination = os.path.join(mkh_data,"proxymeshes")

mkp_pythonw    = os.path.join(mkhPath,"Python","pythonw.exe")
mhstartwrapper = os.path.join(mkhPath,"mhstartwrapper.py")

vsScriptTmpPath = "tmp.txt"

print("path_to_model :   ",modelPath)
print("mkh_source :      ",mkh_source)
print("mkh_destination : ",mkh_destination)
print("mkhPath :",mkhPath )

rotation_angle_x = 1.5708
rotation_angle_z = 0

print(" delete base cube from scene  ......................")
bpy.ops.object.delete(use_global=False, confirm=False)

def mkh_importBody():
    print("makehuman started in background ............")
    print(" open makehuman addon and import makehuman base mesh   ......................")
    bpy.context.scene.mhTabs = 'C'
    bpy.context.scene.MhAdjustPosition = False
    bpy.context.scene.MhImportWhat = 'BODY'
    bpy.ops.mh_community.import_body()


def startMakeHumanProcess(delayTime):
    if platform == "linux" or platform == "linux2"  or platform == "darwin":
        print("Linux version with xterm ...............")
        mkp = subprocess.Popen(['xterm','-hold',"-e",'%s' % mkhPath,'&'])
        #minimizeWindow("makehuman")
    elif platform == "win32":
        print("windows version with visualStudioCode ................")
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        print(mkp_pythonw, mhstartwrapper)
        mhpath=r"C:\Program Files\makehuman-community\makehuman\makehuman.py"
        os.chdir(r"C:\Program Files\makehuman-community\makehuman")
        mkp=subprocess.Popen(["python3",mhpath])
		
    else:
        print("Unknown system ................")
        sys.exit()
    time.sleep(delayTime)
    return mkp

def iaModifyPluginFile(doMinimize,doMKWork):
    print("modify the plugin script ..............")
    oldLines=['doMinimize      = ' ,'doMKWork      = ' ,'vsWeight      = ' , 'modelName     = "' , 'userDocPath   = r"' , 'mkhPath       = r"']

    userDocs= os.path.join(os.path.expanduser("~"),"Documents")

    newLines=['    doMinimize    = '+ str(doMinimize)          + "\n" ,
              '    doMKWork      = '+ str(doMKWork)            + "\n" ,
              '    vsWeight      = '+ str(vsWeight)            + "\n" ,
              '    modelName     = "'+ outputModelFnm          + '"\n',
              '    userDocPath   = r"'+ userDocs + '"\n',
              '    mkhPath       = r"'+ mkhPath +'"\n']
             
    fin = open(vsScriptSrcPath) ;fout = open(vsScriptTmpPath, "wt")
    for line in fin:
        nLine=line
        for j in range (6):
           if oldLines[j] in line:
              print("found: ", line)
              nLine=newLines[j]
              break
        fout.write( nLine )
    fin.close() ;fout.close()
    os.remove(vsScriptSrcPath)
    os.rename(vsScriptTmpPath,vsScriptSrcPath)
    shutil.copyfile( vsScriptSrcPath ,vsScriptPath)

if doCompress:
    print(" compress  meshes  ......................")
    vtkP = subprocess.Popen(["python3",vtkSTLcompressPath,modelPath,compressedModelPath,str(decimate_value)])
    vtkP.wait()

iaModifyPluginFile(1,0)

print(" open makehuman to start the connection   ......................")
mkp = startMakeHumanProcess(delayTime)
mkh_importBody()

print(" import mesh: ",cModelName,compressedModelPath)
bpy.ops.import_mesh.stl(filepath=compressedModelPath,filter_glob="*.stl", files=[{"name": cModelName+".stl", "name":cModelName+".stl"}], directory=path_to_model)

print(" adapt model to makehuman base mesh     ......................")
b_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1))
bpy.ops.transform.resize(value=(0.107514, 0.107514, 0.107514),    orient_type='GLOBAL', orient_matrix=b_matrix, orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.resize(value=(0.0213201, 0.0213201, 0.0213201), orient_type='GLOBAL', orient_matrix=b_matrix, orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.resize(value=(0.411408, 0.411408, 0.411408),    orient_type='GLOBAL', orient_matrix=b_matrix, orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.rotate(value=rotation_angle_x, orient_axis='X', orient_type='GLOBAL', orient_matrix=b_matrix, orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.rotate(value=rotation_angle_z, orient_axis='Z', orient_type='GLOBAL', orient_matrix=b_matrix, orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.resize(value=(1.06056, 1.06056, 1.06056),       orient_type='GLOBAL', orient_matrix=b_matrix, orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

print(" add a texture to the model      ......................")
bpy.ops.mesh.uv_texture_add()

print(" add a vertex group        ......................")
bpy.ops.object.vertex_group_add()
bpy.context.object.vertex_groups[-1].name="body"
bpy.ops.object.editmode_toggle()
verticesToAdd = []
for vertex in bpy.context.object.data.vertices:
    verticesToAdd.append(vertex.index)
bpy.ops.object.editmode_toggle()
bpy.context.object.vertex_groups['body'].add(verticesToAdd,1.0,'ADD')

print("mark object as cloth   ...........")
bpy.ops.makeclothes.mark_as_clothes()

print("save as proxy by generating a unique filename ..........")
bpy.context.object.MhClothesName = outputModelFnm

print("especially for the parts with the holes ........")
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete_loose()
bpy.ops.object.editmode_toggle()
bpy.ops.makeclothes.create_clothes()

print("move object to the proxy folder ................")
shutil.copytree( os.path.join(mkh_source,outputModelFnm)               , os.path.join(mkh_destination,outputModelFnm)         )
shutil.copyfile( os.path.join(mkh_destination,outputModelFnm,outputModelFnm+".mhclo") , os.path.join(mkh_destination,outputModelFnm,outputModelFnm+".proxy") )

try:
 mkp.terminate()
except:
  print("process is not terminated")

if exportSTL:
    iaModifyPluginFile(1,1)

    print(" open makehuman to export stl  ......................")
    mkp = startMakeHumanProcess(60)

    try:
      mkp.terminate()
    except:
      print("process is not terminated")

    iaModifyPluginFile(0,0)

print("STL2MKH is completed !!!")
