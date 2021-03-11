import maya.cmds
import functools
import math 

def createUI(pWindowTitle, pApplyCallback):
    windowID = 'myWindowID'
    if cmds.window(windowID, exists = True):
        cmds.deleteUI( windowID )
    cmds.window( windowID, title = pWindowTitle, resizeToFitChildren = True, width = 500)
    cmds.rowColumnLayout( numberOfColumns = 3, columnWidth = [(1, 75),(2,500),(2,75)], columnOffset = [ (1, 'right', 3) ] )
   
    cmds.text ( label = 'Light group' )
    LGnumber = cmds.intField (value = 1)
    cmds.button ( label = 'Select', command = functools.partial( applyCallback, LGnumber ) )
   
    cmds.text ( label = 'Intensity ' )
    intensityMult = cmds.floatField (value = 1)
    cmds.button ( label = 'Multiply!', command = functools.partial( intenMultCallback, intensityMult ) )
   
    cmds.text ( label = 'Exposure ' )
    exposureAdd = cmds.floatField ()
    cmds.button ( label = 'Add!', command = functools.partial( expoAddCallback, exposureAdd ) )
   
    cmds.text ( label = 'Red ' )
    redMult = cmds.floatField (value = 1, minValue=0, maxValue=1)
    cmds.button ( label = 'Multiply!', command = functools.partial( colMultCallback, redMult, "red" ) )
    
    cmds.text ( label = 'Green ' )
    greenMult = cmds.floatField (value = 1, minValue=0, maxValue=1)
    cmds.button ( label = 'Multiply!', command = functools.partial( colMultCallback, greenMult, "green" ) )
    
    cmds.text ( label = 'Blue ' )
    blueMult = cmds.floatField (value = 1, minValue=0, maxValue=1)
    cmds.button ( label = 'Multiply!', command = functools.partial( colMultCallback, blueMult, "blue" ) )
    
    cmds.text ( label = 'Set LG ' )
    LG_setIndex = cmds.intField (value = 1, minValue=1, maxValue=9)
    cmds.button ( label = 'Set now', command = functools.partial( setLGCallback, LG_setIndex ) )
    
    
    
    cmds.separator(h=10, style = 'none')
    
    cmds.button ( label = 'Check', command = functools.partial( checkCallback ) )
    
    cmds.separator(h=10, style = 'none')
    cmds.separator(h=10, style = 'none')
    
    cmds.button ( label = 'ExpToInt', command = functools.partial( ExpIntCallback ) )
    
    cmds.separator(h=10, style = 'none')
    cmds.separator(h=10, style = 'none')
    
    cmds.button ( label = 'IntToExp', command = functools.partial( IntExpCallback ) )
    cmds.separator(h=10, style = 'none')
    
    
    cmds.separator(h=25, style = 'none')
    cmds.separator(h=25, style = 'none')
    cmds.separator(h=25, style = 'none')
    
    
    
    cmds.text ( label = 'Intensity' )
    cmds.text ( label = 'Exposure' )
    cmds.separator(h=10, style = 'none')
    
    intValueA = cmds.floatField (value = 1)
    expValueA = cmds.floatField (value = 0)
    cmds.button ( label = 'IntToExp', command = functools.partial( transIntExpCallback, intValueA,  expValueA) )
    
    intValueB = cmds.floatField (value = 1)
    expValueB = cmds.floatField (value = 0)
    cmds.button ( label = 'ExpToInt', command = functools.partial( transExpIntCallback, intValueB,  expValueB) )
    
    
   
    cmds.showWindow()
   
def applyCallback ( LGnumber, *pArgs ):  
    lightGroupNumber = str( cmds.intField(LGnumber, query = True, value = True) )
    sel_obj = cmds.ls( selection=True )
    if not sel_obj:
        cmds.warning( "Select LIGHTS grp first" )
    else:
        childNodes = cmds.listRelatives( sel_obj, allDescendents=True )
        cmds.select( clear=True )
        for x in childNodes:
            attrLightGroupExist = maya.cmds.attributeQuery('light_group', node=x, exists=True)
            if attrLightGroupExist:
                light_group_index = cmds.getAttr (x+'.light_group')
                print x
                print light_group_index
                if light_group_index == lightGroupNumber:
                    xTrans = cmds.listRelatives(x, parent = True )
                   
                    cmds.select(xTrans, add=True )
       
def intenMultCallback ( intensityMult, *pArgs ):  
    multiplierVal = cmds.floatField(intensityMult, query = True, value = True)
    sel_light = cmds.ls( selection=True )
    if not sel_light:
        cmds.warning( "NO LIGHTS selected" )
    else:
        for x in sel_light:
            childLight = cmds.listRelatives( x, type = 'shape' )
            for y in childLight:
                attrLightGroupExist = cmds.attributeQuery('intensity', node=y, exists=True)
                if attrLightGroupExist:
                    currentVal = cmds.getAttr (y+'.intensity')
                    cmds.setAttr (y+'.intensity' , currentVal*multiplierVal)

def expoAddCallback ( exposureAdd, *pArgs ):  
    exposureVal = cmds.floatField(exposureAdd, query = True, value = True)
    sel_light = cmds.ls( selection=True )
    if not sel_light:
        cmds.warning( "NO LIGHTS selected" )
    else:
        for x in sel_light:
            childLight = cmds.listRelatives( x, type = 'shape' )
            for y in childLight:
                attrLightGroupExist = cmds.attributeQuery('exposure', node=y, exists=True)
                if attrLightGroupExist:
                    currentVal = cmds.getAttr (y+'.exposure')
                    cmds.setAttr (y+'.exposure' , currentVal+exposureVal)

def colMultCallback ( colMult, colorChan, *pArgs ):  
    colMulti = cmds.floatField(colMult, query = True, value = True)
    sel_light = cmds.ls( selection=True )
    if not sel_light:
        cmds.warning( "NO LIGHTS selected" )
    else:
        for x in sel_light:
            childLight = cmds.listRelatives( x, type = 'shape' )
            for y in childLight:
                attrLightGroupExist = cmds.attributeQuery('color', node=y, exists=True)
                if attrLightGroupExist:
                    if colorChan == 'red':
                        currentVal = cmds.getAttr (y+'.colorR')
                        cmds.setAttr (y+'.colorR' , currentVal*colMulti)
                    if colorChan == 'green':
                        currentVal = cmds.getAttr (y+'.colorG')
                        cmds.setAttr (y+'.colorG' , currentVal*colMulti)
                    if colorChan == 'blue':
                        currentVal = cmds.getAttr (y+'.colorB')
                        cmds.setAttr (y+'.colorB' , currentVal*colMulti)
                        
def checkCallback ( *pArgs ):  
    sel_obj = cmds.ls( selection=True )
    if not sel_obj:
        cmds.warning( "Select LIGHTS grp first" )
    else:
        childNodes = cmds.listRelatives( sel_obj, allDescendents=True )
        cmds.select( clear=True )
        for x in childNodes:
            attrLightGroupExist = maya.cmds.attributeQuery('light_group', node=x, exists=True)
            if attrLightGroupExist:
                light_group_index = cmds.getAttr (x+'.light_group')
                print x
                print light_group_index
                
def setLGCallback (LG_setIndex, *pArgs ):
    LG_index = cmds.intField(LG_setIndex, query = True, value = True)  
    sel_obj = cmds.ls( selection=True )
    if not sel_obj:
        cmds.warning( "Select LIGHTS grp first" )
    else:
        childNodes = cmds.listRelatives( sel_obj, allDescendents=True )
        cmds.select( clear=True )
        for x in childNodes:
            attrLightGroupExist = maya.cmds.attributeQuery('light_group', node=x, exists=True)
            if attrLightGroupExist:
                cmds.setAttr (x+'.light_group', str(LG_index), type = "string")
                print x
                print LG_index
                
def ExpIntCallback ( *pArgs ):
    sel_obj = cmds.ls( selection=True )
    if not sel_obj:
        cmds.warning( "Select LIGHTS grp first" )
    else:
        childNodes = cmds.listRelatives( sel_obj, allDescendents=True )
        for x in childNodes:
            attrExpExist = maya.cmds.attributeQuery('exposure', node=x, exists=True)
            if attrExpExist :
                currentExp = cmds.getAttr (x+'.exposure')
                if currentExp != 0:
                    attrIntExist = maya.cmds.attributeQuery('exposure', node=x, exists=True)  
                    if attrIntExist :
                        currentInt = cmds.getAttr (x+'.intensity')
                        if currentInt != 0:
                            newInt = currentInt *( 2**currentExp )
                            cmds.setAttr (x+'.exposure', 0)
                            cmds.setAttr (x+'.intensity', newInt)
                        else:
                            cmds.warning(x + " intensity is Zero, no change applied" )
                        
def IntExpCallback ( *pArgs ):
    sel_obj = cmds.ls( selection=True )
    if not sel_obj:
        cmds.warning( "Select LIGHTS grp first" )
    else:
        childNodes = cmds.listRelatives( sel_obj, allDescendents=True )
        for x in childNodes:
            attrIntExist = maya.cmds.attributeQuery('intensity', node=x, exists=True)
            if attrIntExist :
                currentInt = cmds.getAttr (x+'.intensity')
                if currentInt != 1:
                    attrExpExist = maya.cmds.attributeQuery('exposure', node=x, exists=True)  
                    if attrExpExist :
                        currentExp = cmds.getAttr (x+'.exposure')
                        newExp = currentExp +( math.log(currentInt,2) )
                        cmds.setAttr (x+'.intensity', 1)
                        cmds.setAttr (x+'.exposure', newExp)
                        
                        
def transIntExpCallback (intValueA,expValueA,*pArgs ):
    intVal = cmds.floatField(intValueA, query = True, value = True)
    expVal = cmds.floatField(expValueA, query = True, value = True)
    totalInt = intVal *( 2**expVal )
    newExpVal =  math.log(totalInt,2)
    cmds.floatField(expValueA, edit = True, value = newExpVal)
    
    

def transExpIntCallback (intValueB,expValueB,*pArgs ):
    intVal = cmds.floatField(intValueB, query = True, value = True)
    expVal = cmds.floatField(expValueB, query = True, value = True)
    totalInt = intVal *( 2**expVal )
    newIntVal =  totalInt /( 2**expVal )
    cmds.floatField(intValueB, edit = True, value = totalInt)

createUI( 'light group selector', applyCallback )
    
        
        
        
cmds.select( clear=True )
