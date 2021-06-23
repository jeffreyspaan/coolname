from enum import Enum, IntEnum
import operator

class Operator(Enum):
    # Binary operators:
    #       Arithmetic operators:
    ADD = 1     # +
    SUB = 2     # -
    MUL = 3     # *
    DIV = 4     # /
    MOD = 5     # %

    #       Relational operators ("and" and "or" ommited):
    LT = 6      # <
    LE = 7      # <=
    GT = 8      # >
    GE = 9      # >=
    EQ = 10     # ==
    NE = 11     # !=

    # Monary operators:
    #       Arithmetic operators:
    NEG = 12    # -

    #       Relational operators:
    NOT = 13    # !

    def is_binop(self):
        return self.value >= Operator.ADD.value and \
               self.value <= Operator.NE.value

    def is_monop(self):
        return self.value == Operator.NOT.value or \
               self.value == Operator.NEG.value

    def is_arithmetic(self):
        return (self.value >= Operator.ADD.value and \
                self.value <= Operator.MOD.value) or \
               (self.value == Operator.NEG.value)

    def is_relational(self):
        return (self.value >= Operator.LT.value and \
                self.value <= Operator.NE.value) or \
               (self.value == Operator.NOT.value)

    def sign(self):
        if      self.value == Operator.ADD.value:   return '+'
        elif    self.value == Operator.SUB.value:   return '-'
        elif    self.value == Operator.MUL.value:   return '*'
        elif    self.value == Operator.DIV.value:   return '/'
        elif    self.value == Operator.MOD.value:   return '%'
        elif    self.value == Operator.LT.value:    return '\<'
        elif    self.value == Operator.LE.value:    return '\<='
        elif    self.value == Operator.GT.value:    return '\>'
        elif    self.value == Operator.GE.value:    return '\>='
        elif    self.value == Operator.EQ.value:    return '=='
        elif    self.value == Operator.NE.value:    return '!='
        elif    self.value == Operator.NEG.value:   return '-'
        elif    self.value == Operator.NOT.value:   return '!'

    def fun(self):
        # TODO: differentiate between / and //
        if      self.value == Operator.ADD.value:   return operator.add
        elif    self.value == Operator.SUB.value:   return operator.sub
        elif    self.value == Operator.MUL.value:   return operator.mul
        elif    self.value == Operator.DIV.value:   return operator.truediv
        elif    self.value == Operator.MOD.value:   return operator.mod
        elif    self.value == Operator.LT.value:    return operator.lt
        elif    self.value == Operator.LE.value:    return operator.le
        elif    self.value == Operator.GT.value:    return operator.gt
        elif    self.value == Operator.GE.value:    return operator.ge
        elif    self.value == Operator.EQ.value:    return operator.eq
        elif    self.value == Operator.NE.value:    return operator.ne
        elif    self.value == Operator.NEG.value:   return operator.neg
        elif    self.value == Operator.NOT.value:   return operator.not_

    def compute(self, inputs):
        """
        Expects inputs in the form:
        {'LHS': 0, 'RHS':1}
        {''}
        """

        if self.is_monop():
            if len(inputs) == 1:
                return self.fun()(list(inputs.values())[0])
            else:
                pass
                # TODO: log error

        elif self.is_binop():
            if len(inputs) == 2 and 'LHS' in inputs and 'RHS' in inputs:
                LHS = inputs.get('LHS')
                RHS = inputs.get('RHS')

                if type(LHS) is not type(RHS):
                    pass
                    # TODO: log error

                return self.fun()(LHS, RHS)
            else:
                pass
                # TODO: log error
