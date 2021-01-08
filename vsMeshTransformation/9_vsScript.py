#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehumancommunity.org/

**Github Code Home Page:**    https://github.com/makehumancommunity/

**Authors:**           Joel Palmius, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2020

**Licensing:**         AGPL3

    This file is part of MakeHuman (www.makehumancommunity.org).

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


Abstract
--------

TODO
"""

# We need this for gui controls
import gui3d
import mh
import gui
import log
import os
class vsScriptTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'vsScript')

        box = self.addLeftWidget(gui.GroupBox('vsScript'))
        self.category=category
        # We add a button to the current task
        # A button just fires an event when it is clicked, if a selected texture is specified,
        # it is used while the mouse is down on the button
        self.vsWeight_gui      = 1.0
        self.modelName_gui    = "T1_large_s_mkh"
        self.userDocPath_gui   = r"C:\Users\Bekki\Documents"
        self.mkhPath_gui       = r"c:\Program Files\makehuman-community"

        self.aTextEdit    = box.addWidget(gui.TextEdit(text='add model name'))
        self.aButton      = box.addWidget(gui.Button('Load MKH Model'))
        self.bButton      = box.addWidget(gui.Button('Export STL Model'))

        self.pushed = 0
        self.aButtonLabel = box.addWidget(gui.TextView('Pushed 0 times'))
        #self.loadRunScript()

        @self.aButton.mhEvent
        def onClicked(event):
            #loadProxy(gui3d.app, 0.88,"T3_s_mkh",r"C:\Users\Bekki\Documents",  r"c:\Program Files\makehuman-community")
            loadProxy(gui3d.app, self.vsWeight_gui , self.modelName_gui,self.userDocPath_gui, self.mkhPath_gui)

        @self.bButton.mhEvent
        def onClicked(event):
             exportProxy(gui3d.app, self.modelName_gui)

        # We want the slider to start from the middle
        self.aSlider      = box.addWidget(gui.Slider(value=0.5, label=['Change Weight',' %.2f']))

        self.aSliderLabel = box.addWidget(gui.TextView('Value is 0.5'))

        @self.aSlider.mhEvent
        def onChange(value):
            self.aSliderLabel.setTextFormat('Weight value is %f', value)
            self.aProgressBar.setProgress(value)

        # we also create a progressbar, which is updated as the slider moves

        self.aProgressBar = box.addWidget(gui.ProgressBar())
        self.aProgressBar.setProgress(0.5)

    def storeMesh(self, human):
        log.message("Storing mesh status")
        self.meshStored = human.meshData.coord.copy()
        self.meshStoredNormals = human.meshData.vnorm.copy()

    def restoreMesh(self, human):
        human.meshData.coord[...] = self.meshStored
        human.meshData.vnorm[...] = self.meshStoredNormals
        human.meshData.markCoords(coor=True, norm=True)

    def onShow(self, event):
        gui3d.app.statusPersist('This is vsScript plugin; see plugins/9_vsScript.py')

    def onHide(self, event):
        gui3d.app.statusPersist('')


category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements
def load(app):
    log.message("=======================================================")
    log.message("             Automating makehuman process")
    log.message("=======================================================")
    #minimise the window ....
    category = app.getCategory('Utilities')
    taskview = category.addTask(vsScriptTaskView(category))
 
    doMinimize    = 0
    doMKWork      = 0
    vsWeight      = 1.0
    modelName     = "T3_large_s_mkh"
    userDocPath   = r"C:\Users\Bekki\Documents"
    mkhPath       = r"c:\Program Files\makehuman-community"
    
    vsScriptTaskView.vsWeight_gui    = vsWeight
    vsScriptTaskView.modelName_gui   = modelName
    vsScriptTaskView.userDocPath_gui = userDocPath
    vsScriptTaskView.mkhPath_gui     = mkhPath

    if doMinimize:
       app.mainwin.showMinimized()
    
    
    stlExportPath = mkhPath + "/plugins/9_export_stl/__init__.py'"

    if doMKWork:
        try:
            loadProxy(app, vsWeight,modelName,userDocPath, mkhPath)
        except:
           log.message("error during loading proxy ...................")
        try:
           exportProxy(app, modelName)
        except:
           log.message("error during saving stl ..................")
    #TODO: try app. instead of self.
    #app.mainwin.show()

    #app.mainwin.hide()
    #app.mainwin.close()
    #app.closeAllWindows()


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements
def unload(app):
    print("unloading  .................")
    # #get category files

def loadProxy(app,vsWeight,modelName,userDocPath, mkhPath):
    path_to_proxy=os.path.join(userDocPath,"makehuman","v1py3","data","proxymeshes",modelName,modelName+".proxy")
    #find right category
    category= app.getCategory('Geometries')
    #find right task
    task=category.getTaskByName('Topologies')
    #select Proxy
    task.selectProxy(path_to_proxy)
    #set weight
    task.human.setWeight(vsWeight)
    #remove eye proxy
    eyes=category.getTaskByName('Eyes')
    eyes.deselectAllProxies()    


def exportProxy(app, modelName):
    log.message("export stl ..............")
    file=app.getCategory('Files')

    file.export.fileentry.setText(modelName+"_mh")
    stl_exporter=file.export.formats[7]
    exporter=stl_exporter[0]
    select_exporter=stl_exporter[1]
    widget=stl_exporter[2]

    select_exporter.setSelected(1)
    widget.setChecked(1)

    file.export.fileentry.confirm.click()
    log.message("Stl object has been generated")

    
