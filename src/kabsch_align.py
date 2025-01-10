import bpy
import numpy as np
import bmesh
import mathutils
import copy


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


if __name__ == "__main__":
    # get all objects
    objs = bpy.data.objects

    # get selected vertices for Obj0
    cube0 = objs["Obj0"]
    c0_mesh = bmesh.from_edit_mesh(cube0.data)
    points_c0 = np.asarray(
        [
            cube0.matrix_world @ v.co
            for v in c0_mesh.select_history
            if isinstance(v, bmesh.types.BMVert)
        ]
    )
    # get selected vertices for Obj1
    cube1 = objs["Obj2"]
    c1_mesh = bmesh.from_edit_mesh(cube1.data)
    points_c1 = np.asarray(
        [
            cube1.matrix_world @ v.co
            for v in c1_mesh.select_history
            if isinstance(v, bmesh.types.BMVert)
        ]
    )
    # calculate the rotation matrix and the centroids
    c0, c1, rmat = rotamat(points_c0, points_c1)

    # apply rotation matrix and translation to one object and get the new coordinates
    cube1_trans = (
        rmat
        @ (np.asarray([cube1.matrix_world @ v.co for v in cube1.data.vertices]) - c1).T
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
