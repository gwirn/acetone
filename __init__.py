import bpy

bl_info = {
    "name": "Acetone",
    "author": "gwirn",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N > Acetone > Superimpose",
    "description": "Superimpose two objects",
    "warning": "",
    "doc_url": "",
    "category": "Superimpose Object",
}


def get_object_items(self, context):
    return [(obj.name, obj.name, "") for obj in bpy.data.objects]


def register():
    bpy.types.Scene.object_static = bpy.props.EnumProperty(
        items=get_object_items, name="Static"
    )
    bpy.types.Scene.object_mobile = bpy.props.EnumProperty(
        items=get_object_items, name="Mobile"
    )
    from . import ui

    bpy.utils.register_class(ui.AcetonePanel)
    bpy.utils.register_class(ui.AcetoneOperator)
    bpy.types.Scene.rmsd = bpy.props.FloatProperty(name="Result")
    bpy.types.Scene.rmsd_done = bpy.props.BoolProperty(name="RMSD Done", default=False)


def unregister():
    del bpy.types.Scene.object_static
    del bpy.types.Scene.object_mobile
    from . import ui

    bpy.utils.unregister_class(ui.AcetonePanel)
    bpy.utils.unregister_class(ui.AcetoneOperator)
    del bpy.types.Scene.rmsd
    del bpy.types.Scene.rmsd_done


if __name__ == "__main__":
    register()
