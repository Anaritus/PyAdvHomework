from constants import TEST_TABLES, IMAGE, ARTIFACTS_DIR
from texformatter import pngToTeX, tableToTeX
from inspect import cleandoc


with open(ARTIFACTS_DIR + 'main.tex', 'w') as fout:
    fout.write(
        cleandoc(
            r"""
        \documentclass{article}
        \usepackage{graphicx}

        \begin{document}
        """
        )
    )
    fout.write('\n')
    fout.write('\n'.join([tableToTeX(t) for t in TEST_TABLES]))
    fout.write('\n')
    fout.write(pngToTeX(IMAGE))
    fout.write('\n')
    fout.write(r'\end{document}')
