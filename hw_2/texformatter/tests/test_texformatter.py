from texformatter import tableToTeX, pngToTeX
from inspect import cleandoc

testTables = [
    [['one', 'and two'], ['and three', 'and four'], ['also', 'extra row']],
    [['this', 'one is', 'wide', 'but one dimensional']],
    [['this'], ['one is'], ['long'], ['but one dimensional']],
]

test_png = 'test.png'


def test_tableToTex():
    assert tableToTeX(testTables[0]) == cleandoc(
        r"""
        \begin{center}
          \begin{tabular}{ c c }
            one & and two \\
            and three & and four \\
            also & extra row
          \end{tabular}
        \end{center}
        """
    )


def test_pngToTeX():
    assert pngToTeX(test_png) == cleandoc(
        r"""
         \begin{figure}[h!]
         \centering
           \includegraphics[width=0.5\textwidth]{test.png}
           \caption{test}
         \end{figure}
        """
    )
