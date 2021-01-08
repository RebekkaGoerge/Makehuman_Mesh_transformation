# Makehuman_Mesh_transformation
The following script and plugin for makehuman can be used to load an arbitrary person mesh (.stl) into makehuman by generating a proxy. The weight of the proxy can be modified via the script and afterwards is exported back to an stl file. Furthermore the proxy can also be modified manually in makehuman. The script and plugin uses makehuman and blender and some plugins. 

# MakeHuman
The following script and plugin for makehuman can be used to load an arbitrary person mesh (.stl) into makehuman by generating a proxy. The weight of the proxy can be modified via the script and afterwards is exported back to an stl file. Furthermore the proxy can also be modified manually in makehuman. The script and plugin uses makehuman and blender and some plugins. 

## Table of Contents  
1. [Getting start](#gettingStart)  
2. [Use the plugin](#runTheCode)  
3. [How does the scripts work](#script)  

<a name="gettingStart"></a>

## Getting started

Download the stable release [makehuman version 1.2.0](http://www.makehumancommunity.org/content/downloads.html) and follow the installation instructions. For Linux you might need to build the code up from source. 

Download [blender 2.9](https://www.blender.org/download/) and follow the installation instructions, also add blender to the path variables.

### Download the following plugins for blender:
* [makehuman plugin for blender](http://download.tuxfamily.org/makehuman/plugins/makehuman-plugin-for-blender-latest.zip) 
* [makeSkin plugin](http://download.tuxfamily.org/makehuman/plugins/makeskin-latest.zip)
* [makeClothes2 plugin](http://download.tuxfamily.org/makehuman/plugins/makeclothes2-latest.zip)

Install the blender plugins: 
1. Open the preferences in blender:  

<img src="https://user-images.githubusercontent.com/62305343/103997024-e0026980-519a-11eb-92f7-cc241d8ec832.png" alt="blender_addons_step1" width="600"/>


2. Press the install button:

<img src="https://user-images.githubusercontent.com/62305343/103997031-e2fd5a00-519a-11eb-8776-5dffafc90150.png" alt="blender_addons_step2" width="600"/>


3. Search for the zip files of the downloaded addons and press install:

<img src="https://user-images.githubusercontent.com/62305343/103997036-e4c71d80-519a-11eb-8bc9-066c7102e791.png" alt="blender_addons_step3" width="600"/>


4. By pressing "N" the makehuman bar appears at the right side:

<img src="https://user-images.githubusercontent.com/62305343/103997470-661eb000-519b-11eb-97a4-dcc8c81c8d4d.png" alt="blender_makehuman" width="600"/>


### Download the following plugins for makehuman: 

* [Socket plugin](http://download.tuxfamily.org/makehuman/plugins/socket-latest.zip)

* [MHAPI](http://download.tuxfamily.org/makehuman/plugins/mhapi-latest.zip)

* [9_vsScript plugin]()



Download the plugins and copy them to the makehuman plugin directory (~\makehuman\v1py3\plugins). Activate them either in the settings.inl or in the makehuman gui (see following pictures). In Windows MHAPI might be already installed.

1. The socket plugin and the MHAPI are makehuman plugins and can be activated in the normal plugin folder. 

<img src="https://user-images.githubusercontent.com/62305343/103997466-64ed8300-519b-11eb-8de7-96f53de4aae0.png" alt="Install plugins" width="600"/>

2. As the vs_Script is a user plugin, it needs to be activated as user plugin. 

<img src="https://user-images.githubusercontent.com/62305343/103997415-569f6700-519b-11eb-8b17-0d3339c42c89.png" alt="Install plugins" width="600"/>


<a name="runTheCode"></a>

## Run the code 

1. Open the file "vs01_STL2MakeHuman.py" from this repository
2. Adapt the paramters *projectPath*, *modelName*, *vsWeight* and *decimateValue* according to your model and project 
3. Save the file 
4. If you have run the code before with the same model name, clean the clothes, proxymesh and export folder 
5. Run the code from the console as administrator with the following command: **blender --background --python vs01_STL2MakeHuman.py**
6. The code needs some minutes to run, afterwards you can find the created proxy from your mesh in the proxymesh folder
7. if the parameter *export stl* is set to true, you can also find the modified stl file (according to the parameters you set in the beginning) in the export folder  

<a name="scripts"></a>

## How does it work:

Scripts:
- vs01_STL2Makehuman.py 
- 09_vsScript.py


### vs01_STL2Makehuman:

**parameters (set through the user):**

* *project path* : path to the folder of the mesh 
* *model name*: name of the mesh
* *doCompression*: compression or not (mesh needs to have a similar size to the mh base mesh)
* *decimateValue*: value how much mesh is compressed
* *exportSTL*: 1 if a stl file with modified weight should be generated, 0 if only the makehuman proxymesh needs to be generated
* *vsWeight*: a value between 0 and 1 


**methods:**
* *startMakeHumanProcess(delay time)*:
  
  makehuman is started from the code with a delay time until the system is loaded
* *iaModifyPluginFile(doMinimize, doMKWork)* 

  changes the plugin *09_vsScript* according to the parameters
  if doMinimize:  the makehuman window is minimized after the plugin has loaded
  if doMKWork:    the plugin loads the generated mesh to makehuman, modifies it and exports the mesh back to stl

* *mkh_importBody()*

 imports makehuman base mesh 


### 09_vsScript

**methods**
* load(app): 

  this method is called when the plugin is loaded into makehuman 
  minimizes the window 
  calls loadProxy and exportProxy 

* loadProxy(app,vsWeight,modelName,userDocPath, mkhPath): 

  loads the proxy with the model name and change the weight according to the defined weight 

* exportProxy(app, modelName):

  export the proxy to an stl file and stores it 

* unload(app): 

  this method is called if th plugin is unloaded 


**Workflow**

The script is executed with blender. After setting up the parameters, the mesh is compressed. This needs to be done, in order that the loaded mesh has a similar size to the human base mesh. The method *iaModifyPluginFile(1,0)* and *startMakeHumanProcess* are called and afterwards makehuman is started and the window is minimized. Now blender can connect to makehuman and can import the mh base mesh with the method *mkh_importBody*. Afterwards, the compressed stl model is also imported into blender. The model is transformed so that it fits in orientation, rotation and size to the makehuman model (this need to be adapted if the model differs from our standarts). The model is extended through an uv map and the vertex are grouped into a vertex group. The model is marked as "clothes" and loose vertices are removed. Afterwards, the create_clothes() method from the makeclothes plugin is called. After a succesful creation of the clothes, they should be stored in the ~\makehuman\v1py3data\clothes folder. We copy this folder to the ~\makehuman\v1py3\data\proxymesh folder. Furthermore, we copy the modelName.mhclo file to a modelName.proxy file. Now we have our makehuman proxy. For now makehuman is closed. 

If the *export_stl* variable is set to true in the next part we modify our plugin *09_vsScript.py* by calling *iaModifyPluginFile(1,1)*, so next time makehuman is started, the window will be minimized and also our new proxy will be loaded, modified and exported. Here we also transfer the model name and the values to modify the model. After modifing the plugin, we restart makehuman. By restarting makehuman the plugin is also loaded. The plugin minimize the makehuman window, and tries to load the mesh with the model name and the selected weight. Afterwards, it tries to export the modified model to an stl file. And finally closes makehuman.  The exported file can be found in the export folder (~\makehuman\v1py3\exports). 
