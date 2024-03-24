from inspect import cleandoc


def handleEqualShape(self, other):
    if self.shape != other.shape:
        errormsg = cleandoc(
            f"""
            shapes do not align:
            first shape is {self.shape},
            other shape is {other.shape}
            """
        )
        raise ValueError(errormsg)


def handleMatMulShape(self, other):
    if self.shape[1] != other.shape[0]:
        errormsg = cleandoc(
            f"""
                shapes do not align:
                first shape is {self.shape},
                other shape is {other.shape}
                """
        )
        raise ValueError(errormsg)
