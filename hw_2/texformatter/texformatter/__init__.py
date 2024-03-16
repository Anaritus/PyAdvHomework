from .util import formatRow
from inspect import cleandoc


def tableToTeX(arr):
    """
    Creates Valid tex table from two dimensional arr.
    """
    n = len(arr)
    if not n:
        return ''
    m = len(arr[0])

    start = cleandoc(
        rf"""
        \begin{{center}}
          \begin{{tabular}}{{ {"c " * m}}}
        """
    )
    middle_separator = r' \\' + '\n'
    middle = middle_separator.join([formatRow(row) for row in arr])
    end = cleandoc(
        r"""
          \end{tabular}
        \end{center}
        """
    )

    return '\n'.join([start, middle, end])


def pngToTeX(png):
    """
    Creates valid image in tex from filename.
    """
    png_name = png[: png.rfind('.')].replace('$', r'\$').replace('_', '-')
    return cleandoc(
        rf"""
        \begin{{figure}}[h!]
        \centering
          \includegraphics[width=0.5\textwidth]{{{png}}}
          \caption{{{png_name}}}
        \end{{figure}}
        """
    )
