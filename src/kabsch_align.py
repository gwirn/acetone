import bpy
import numpy as np
import bmesh
import mathutils
import copy

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


def shift(
    arr: np.ndarray[tuple[int, int], np.dtype[int]],
) -> tuple[
    np.ndarray[tuple[int], np.dtype[int | float]],
    np.ndarray[tuple[int, int], np.dtype[int | float]],
]:
    """shift coordinated based on the shift of their centroid to the origin
    :parameter
        - arr:
          the array of coordinates to be shifted
    :return
        - centroid
          the centroid of the array
        - arr_shifted
          the shifted array
    """
    centroid = np.mean(arr, axis=0)
    arr_shifted = arr - centroid
    return centroid, arr_shifted


def rotamat(
    system1: np.ndarray[tuple[int, int], np.dtype[int]],
    system2: np.ndarray[tuple[int, int], np.dtype[int]],
) -> tuple[
    np.ndarray[tuple[int], np.dtype[int | float]],
    np.ndarray[tuple[int], np.dtype[int | float]],
    np.ndarray[tuple[int, int], np.dtype[int]],
]:
    """kabsch algorithm to find the optimal rotation matrix
    :parameter
        - system1, system2:
          coordinate systems for which the optimal alignment should be calculated
    :return
        - U:
          the rotation matrix
        - c_s1, c_s2:
          centroids of each system
    """
    # shift the coordinates to the origin
    c_s1, system1 = shift(system1)
    c_s2, system2 = shift(system2)

    # covariance matrix
    cov_mat = np.dot(np.transpose(system1), system2)
    # singular value decomposition
    V, S, W = np.linalg.svd(cov_mat)

    # check for right-handedness of the coordinate system
    d = (np.linalg.det(V) * np.linalg.det(W)) < 0.0
    if d:
        S[-1] = -S[-1]
        V[:, -1] = -V[:, -1]

    # create Rotation matrix U
    U = np.dot(V, W)
    return c_s1, c_s2, U


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
    bl_idname = "object.align"
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
        c0, c1, rmat = rotamat(points_c0, points_c1)

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


def get_object_items(self, context):
    return [(obj.name, obj.name, "") for obj in bpy.data.objects]


def register():
    bpy.types.Scene.object_static = bpy.props.EnumProperty(
        items=get_object_items, name="Static"
    )
    bpy.types.Scene.object_mobile = bpy.props.EnumProperty(
        items=get_object_items, name="Mobile"
    )
    bpy.utils.register_class(SpectatorPanel)
    bpy.utils.register_class(SpectatorOperator)


def unregister():
    del bpy.types.Scene.object_static
    del bpy.types.Scene.object_mobile
    bpy.utils.unregister_class(SpectatorPanel)
    bpy.utils.unregister_class(SpectatorOperator)


if __name__ == "__main__":
    register()
