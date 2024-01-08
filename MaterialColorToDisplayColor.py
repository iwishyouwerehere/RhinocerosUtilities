#https://discourse.mcneel.com/t/how-to-set-display-colours-to-material-colours/166067/3
import Rhino
import scriptcontext
import System
def CreateMaterialFromDisplayColor():
    rhino_objects = scriptcontext.doc.Objects
    for obj in rhino_objects:
        try:
            display_color = obj.Attributes.DrawColor(scriptcontext.doc)
            material_index = scriptcontext.doc.Materials.Add()
            material = scriptcontext.doc.Materials[material_index]
            material.DiffuseColor = System.Drawing.Color.FromArgb(display_color.A, display_color.R, display_color.G, display_color.B)
            material.CommitChanges()
            obj.Attributes.MaterialIndex = material_index
            obj.Attributes.MaterialSource = Rhino.DocObjects.ObjectMaterialSource.MaterialFromObject
            obj.CommitChanges()
        except Exception as e:
            print("An error occurred while processing object {obj.Id}: {e}")
CreateMaterialFromDisplayColor()
