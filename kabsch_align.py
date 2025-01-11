import numpy as np


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
    pass
