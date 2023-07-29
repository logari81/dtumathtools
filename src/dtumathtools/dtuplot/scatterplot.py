from sympy import Matrix
from sympy.external import import_module
from spb.functions import plot_list, plot3d_list
from spb.backends.base_backend import Plot
from numpy import ndarray


def scatter(*args, **kwargs):
    """Create a plot with one/multiple point(s). Similar to plt.scatter.

    Args:
        points (MatrixBase, ndarray, list, float): The point(s) to scatter. If multiple points are given, simply list them as multiple arguments, each being Matrix, ndarray, or list.
        rendering_kw (dict, optional): A dictionary forwarded to dtuplot.plot(), see SPB docs for reference.
        color (str, optional): A string to set the color of the points with. With no argument color = 'blue'.
        show (bool, optional): Boolean, if 'True': show plot, other just return object without plotting. Defaults to 'True'.

    Returns:
        Plot: The plot containing the points.
    """

    np = import_module("numpy")
    warnings = import_module("warnings")

    def warning_formatter(msg, *args, line=None, **kwargs):
        return str(msg)

    warnings.formatwarning = warning_formatter

    # format all arguments
    dim = 0
    args = list(args)
    otherargs = []
    matrixlist = []
    for i in range(len(args)):
        if type(args[i]) in (list, tuple):
            args[i] = np.array(args[i])
            dim += 1
        elif type(args[i]) == np.ndarray:
            if len(args[i].shape) > 1:
                warnings.warn(
                    f"np.array with more than 1 dimension ({len(args[i].shape)} dimensions was found) has been flattened!"
                )
            args[i] = args[i].flatten()
            dim += 1
        elif type(args[i]) in [float, int]:
            args[i] = np.array([args[i]])
            dim += 1
        elif type(args[i]) == type(Matrix()):
            matrixlist.append(args[i])
        else:
            try:
                # symbolic expression not multiplied fully
                args[i] = np.array([float(args[i])])
                dim += 1
            except:
                otherargs.append(args[i])

    # if entries are matricies, get them into right format
    if len(matrixlist) > 0:
        assert dim == 0, "Cannot mix matrix and non-matrix arguments!"
        firstshape = matrixlist[0].shape
        assert len(firstshape) in [1, 2], "Matrix must be 1D or 2D!"
        assert (
            min(firstshape) == 1
        ), "Matrix must not have multiple dimensions different from size 1!"
        dim = max(firstshape)
        newargs = [np.array([])] * dim
        for i in range(len(matrixlist)):
            assert (
                matrixlist[i].shape == firstshape
            ), "All matrices must have the same shape!"
            for j in range(len(matrixlist[i])):
                newargs[j] = np.append(newargs[j], matrixlist[i][j])
        args = newargs
        args.extend(otherargs)

    assert dim in [2, 3], "scatterplot only supports 2D and 3D plots"
    if dim == 2:
        rendering_kw = kwargs.pop("rendering_kw", {})
        markersize = rendering_kw.pop("s", None)
        if markersize is not None:
            rendering_kw.setdefault("markersize", markersize)
        return plot_list(*args, is_point=True, rendering_kw=rendering_kw, **kwargs)
    else:
        return plot3d_list(*args, is_point=True, **kwargs)
