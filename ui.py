import bpy
import numpy as np
import bmesh
import mathutils
import copy
from . import kabsch_align

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


class SpectatorPanel(bpy.types.Panel):
    bl_label = "Spectator"
    bl_idname = "OBJECT_PT_spectator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Spectator"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "object_static")
        layout.prop(scene, "object_mobile")
        layout.operator("object.spectator")


class SpectatorOperator(bpy.types.Operator):
    bl_idname = "object.spectator"
    bl_label = "Align"

    def align(self, context):
        scene = context.scene
        # get all objects
        objs = bpy.data.objects
        # get selected vertices for Obj0
        cube0 = objs[scene.object_static]
        c0_mesh = bmesh.from_edit_mesh(cube0.data)
        points_c0 = np.asarray(
            [
                cube0.matrix_world @ v.co
                for v in c0_mesh.select_history
                if isinstance(v, bmesh.types.BMVert)
            ]
        )
        # get selected vertices for Obj1
        cube1 = objs[scene.object_mobile]
        c1_mesh = bmesh.from_edit_mesh(cube1.data)
        points_c1 = np.asarray(
            [
                cube1.matrix_world @ v.co
                for v in c1_mesh.select_history
                if isinstance(v, bmesh.types.BMVert)
            ]
        )

        n_pc0 = len(points_c0)
        n_pc1 = len(points_c1)
        assert n_pc0 > 0, f"'{scene.object_static}' has no selected points"
        assert n_pc1 > 1, f"'{scene.object_mobile}' has no selected points"
        assert (
            n_pc0 == n_pc1
        ), f"Both objects need the same number of selecte points. Got {len(points_c0)} points for '{scene.object_static}'  but {len(points_c1)} points for '{scene.object_mobile}' "

        c0_mesh.free()
        c1_mesh.free()
        # calculate the rotation matrix and the centroids
        c0, c1, rmat = kabsch_align.rotamat(points_c0, points_c1)

        # apply rotation matrix and translation to one object and get the new coordinates
        cube1_trans = (
            rmat
            @ (
                np.asarray([cube1.matrix_world @ v.co for v in cube1.data.vertices])
                - c1
            ).T
        ).T + c0

        # new mesh to save the transformed coordinates to
        c1_data = cube1.data
        c1_mesh = bmesh.from_edit_mesh(c1_data)

        # update each vertex with the translated and rotated coordinates
        for ci in range(len(cube1_trans)):
            v = c1_mesh.verts[ci]
            co = cube1.matrix_world @ v.co
            co = mathutils.Vector(cube1_trans[ci])
            invert = copy.copy(cube1.matrix_world)
            invert.invert()
            v.co = invert @ co
        # update the mesh
        bmesh.update_edit_mesh(c1_data)

    def execute(self, context):
        self.align(context)
        return {"FINISHED"}


if __name__ == "__main__":
    pass
