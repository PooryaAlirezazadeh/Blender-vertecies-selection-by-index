
import bpy
import bmesh
from bpy.props import (FloatProperty,
                       StringProperty,
                       IntProperty,
                       EnumProperty,
                       FloatVectorProperty,
                       BoolProperty,
                       PointerProperty)
from bpy.types import (Context, Panel,
                       PropertyGroup,
                       AddonPreferences)

bl_info = {
    "name": "Vertices Selector",
    "blender": (2, 80, 0),  
    "category": "3D View",
    "author": "Poorya Alirezazadeh",
    "version": (1, 0, 0),
    "blender": (4, 0, 1),
    "location": "View3D > Sidebar > Vertices Selector",
    "description": "Select vertices based on index",
    "wiki_url": "",
    "category": "Object" }

class MySettings(PropertyGroup):
    my_bool : BoolProperty(
        name = "True or False",
        description = "A bool property",
        default = False
    )
    my_int : IntProperty(
        name = "Set a integer value",
        description = "A integer property",
        default = 1,
        min = 0
    )
    my_float : FloatProperty(
        name = "Set a float value",
        description = "A float property",
        default = 0.5, 
        min = 0.1
    )
    
class VerticesSelection (Panel):
    bl_label = "Vertecies selection by index"
    bl_idname = "PT_VerticesSelectorByIndexPanel"
    bl_category = "Vertecies Selector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
        mytools = context.scene.my_tools
        row.prop(mytools,"my_int",text="Index")
        row = layout.row()
        row.operator("mesh.select_by_index", text="Select Vertices")

class SelectByIndex(bpy.types.Operator):
    bl_idname = "mesh.select_by_index"
    bl_label = "ُSelect vertecies by index"    
    def selectVertecies(index,obj,context):

        bpy.ops.object.mode_set(mode='EDIT')
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)
        bm.select_mode = {"VERT"}
        for v in bm.verts:
            v.select = False
        for v in bm.verts:
            if v.index == index:
                v.select = True
        bmesh.update_edit_mesh(mesh)
        bm.free()
    def execute(self, context):
        my_tools = bpy.context.scene.my_tools
        index = my_tools.my_int
        obj = context.active_object
        SelectByIndex.selectVertecies(index,obj,context)
        return {"FINISHED"}
    
classes = (
    MySettings,
    VerticesSelection,
    SelectByIndex
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_tools = PointerProperty(type=MySettings)
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_tools
if __name__ == "__main__":
    register()
    