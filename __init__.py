import bpy

bl_info = {
    "name": "Spectator",
    "author": "gwirn",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N > Item > Spectator > Align",
    "description": "Align two objects",
    "warning": "",
    "doc_url": "",
    "category": "Align Object",
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

    bpy.utils.register_class(ui.SpectatorPanel)
    bpy.utils.register_class(ui.SpectatorOperator)


def unregister():
    del bpy.types.Scene.object_static
    del bpy.types.Scene.object_mobile
    from . import ui

    bpy.utils.unregister_class(ui.SpectatorPanel)
    bpy.utils.unregister_class(ui.SpectatorOperator)


if __name__ == "__main__":
    register()
