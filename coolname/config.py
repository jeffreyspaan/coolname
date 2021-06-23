from .operator_ import *
import math

class Config:
    class Latency:
        computation = {
            Operator.ADD: 1,
            Operator.SUB: 1,
            Operator.MUL: 3,
            Operator.DIV: 24,
            Operator.MOD: 24,
            Operator.LT: 1,
            Operator.LE: 1,
            Operator.GT: 1,
            Operator.GE: 1,
            Operator.EQ: 1,
            Operator.NE: 1,
            Operator.NEG: 0,
            Operator.NOT: 1
        }

        eta = 0

        mu_str = 'lambda n: math.log(n)'
        mu = eval(mu_str)

        mux_str = 'lambda n: math.log(n/4)'
        mux = eval(mux_str)

        combine_str = 'lambda n: math.log(n)/2'
        combine = eval(combine_str)

        xor_str = 'lambda n: math.log(n)/2'
        xor = eval(xor_str)

        mem_load = 8
        mem_store = 8
        communication = 1

    class Energy:
        computation = {
            Operator.ADD: 100,
            Operator.SUB: 100,
            Operator.MUL: 100,
            Operator.DIV: 100,
            Operator.MOD: 100,
            Operator.LT: 100,
            Operator.LE: 100,
            Operator.GT: 100,
            Operator.GE: 100,
            Operator.EQ: 100,
            Operator.NE: 100,
            Operator.NEG: 100,
            Operator.NOT: 100
        }

        eta = 100

        mu_str = 'lambda n: n*100'
        mu = eval(mu_str)

        mux_str = 'lambda n: n*100'
        mux = eval(mux_str)

        combine_str = 'lambda n: n*100'
        combine = eval(combine_str)

        xor_str = 'lambda n: n*100'
        xor = eval(xor_str)

        mem_load = 100
        mem_store = 100
        communication = 0