from nodes import *
from control import *
from memory import *

def test_monary():
    """
     ╭───╮
     │123│
     ╰─┬─╯
       │
       │
     ┌─▼─┐
     │ - ◄╌╌T
     └─┬─┘
       │
       │
    ┌──▼──┐
    │drain│
    └─────┘
    """

    c1 = ContinualConstant(123, name='CC1')
    comp = Computation(Operator.NEG, name='COMP')
    drain = Drain()

    w1 = Wire(c1, comp, Input.value_types.DATA)

    c1.add_output(w1)
    comp.add_input(w1)

    ic1 = IntegratedConstant(True, Input.value_types.PREDICATE)
    comp.add_input(ic1)

    w2 = Wire(comp, drain, Input.value_types.DATA)

    comp.add_output(w2)
    drain.add_input(w2)

    return [c1,comp,drain]

def test_binary():
    """
    ╭───╮ ╭───╮
    │ 1 │ │ 2 │
    ╰──┬╯ ╰┬──╯
       │   │
       │   │
       ▼───▼
       │ + ◄╌╌T
       └─┬─┘
         │
         │
      ┌──▼──┐
      │drain│
      └─────┘

    Output: 3
    """
    c1 = ContinualConstant(1, name='CC1')
    c2 = ContinualConstant(2, name='CC2')
    comp = Computation(Operator.ADD, name='COMP')
    drain = Drain()

    w1 = Wire(c1, comp, Input.value_types.DATA, name='LHS')
    w2 = Wire(c2, comp, Input.value_types.DATA, name='RHS')

    c1.add_output(w1)
    c2.add_output(w2)
    comp.add_input(w1)
    comp.add_input(w2)

    ic1 = IntegratedConstant(True, Input.value_types.PREDICATE)
    comp.add_input(ic1)

    w3 = Wire(comp, drain, Input.value_types.DATA)

    comp.add_output(w3)
    drain.add_input(w3)

    return [c1,c2,comp,drain]

def test_multiplecomps():
    """
          ╭───╮
          │ 1 │
          ╰┬─┬╯
           │ │
           │ │
          ┌▼─▼┐
          │ + ◄╌╌T
          └┬─┬┘
         ┌─┘ └──┐
       ┌─▼─┐ ┌──▼──┐
    T╌╌► - │ │drain│
       └─┬─┘ └─────┘
         │
         │
      ┌──▼──┐
      │drain│
      └─────┘

    Output: 2, -2, 2 ...
    """

    c1 = ContinualConstant(1, name='CC1')
    comp1 = Computation(Operator.ADD, name='COMP1')
    comp2 = Computation(Operator.NEG, name='COMP2')
    drain1 = Drain(name='DRAIN1')
    drain2 = Drain(name='DRAIN2')

    w1 = Wire(c1, comp1, Input.value_types.DATA, name='LHS')
    w2 = Wire(c1, comp1, Input.value_types.DATA, name='RHS')

    c1.add_output(w1)
    c1.add_output(w2)
    comp1.add_input(w1)
    comp1.add_input(w2)

    ic1 = IntegratedConstant(True, Input.value_types.PREDICATE)
    comp1.add_input(ic1)

    w3 = Wire(comp1, drain1, Input.value_types.DATA)

    comp1.add_output(w3)
    drain1.add_input(w3)

    w4 = Wire(comp1, comp2, Input.value_types.DATA)

    comp1.add_output(w4)
    comp2.add_input(w4)

    ic2 = IntegratedConstant(True, Input.value_types.PREDICATE)
    comp2.add_input(ic2)

    w5 = Wire(comp2, drain2, Input.value_types.DATA)

    comp2.add_output(w5)
    drain2.add_input(w5)

    return [c1,comp1,comp2,drain1,drain2]

def test_binaryintegrated():
    """
        1 2
        │ │
       ┌▼─▼┐
       │ + ◄╌╌T
       └─┬─┘
         │
         │
      ┌──▼──┐
      │drain│
      └─────┘

    Output: 3, 3, ...
    """
    comp = Computation(Operator.ADD, name='COMP')
    drain = Drain()

    ic1 = IntegratedConstant(1, Input.value_types.DATA, name='LHS')
    ic2 = IntegratedConstant(2, Input.value_types.DATA, name='RHS')

    comp.add_input(ic1)
    comp.add_input(ic2)

    ic3 = IntegratedConstant(True, Input.value_types.PREDICATE)
    comp.add_input(ic3)


    w3 = Wire(comp, drain, Input.value_types.DATA)

    comp.add_output(w3)
    drain.add_input(w3)

    return [comp,drain]

def test_binaryonetime():
    """
    ╔═══╗ ╔═══╗
    ║ 1 ║ ║ 2 ║
    ╚══╤╝ ╚╤══╝
       │   │
       │   │
       ▼───▼
       │ + ◄╌╌T
       └─┬─┘
         │
         │
      ┌──▼──┐
      │drain│
      └─────┘

    Output: 3, 3, ...
    """
    c1 = OnetimeConstant(1, name='OC1')
    c2 = OnetimeConstant(2, name='OC2')
    comp = Computation(Operator.ADD, name='COMP')
    drain = Drain()

    w1 = Wire(c1, comp, Input.value_types.DATA, name='LHS')
    w2 = Wire(c2, comp, Input.value_types.DATA, name='RHS')

    c1.add_output(w1)
    c2.add_output(w2)
    comp.add_input(w1)
    comp.add_input(w2)

    ic1 = IntegratedConstant(True, Input.value_types.PREDICATE)
    comp.add_input(ic1)

    w3 = Wire(comp, drain, Input.value_types.DATA)

    comp.add_output(w3)
    drain.add_input(w3)

    return [c1,c2,comp,drain]

def test_ETA():
    """
    ╔═══╗
    ║ T ║
    ╚═╤═╝
      ╎123
      ╎ │
     ┌▼─▼┐
     │ETA│
     └─┬─┘
       │
       │
    ┌──▼──┐
    │drain│
    └─────┘

    Output: 123
    """

    c = OnetimeConstant(True)
    eta = ETA()
    drain = Drain()

    ic1 = IntegratedConstant(123, Input.value_types.DATA)
    eta.add_input(ic1)

    w2 = Wire(c, eta, Input.value_types.PREDICATE)
    c.add_output(w2)
    eta.add_input(w2)

    w3 = Wire(eta, drain, Input.value_types.DATA)
    eta.add_output(w3)
    drain.add_input(w3)

    return [c,eta,drain]

def test_Mu():
    """
     ╔═══╗
     ║123║
     ╚═╤═╝
       │
       │  ┌───────┐
    ┌──▼──▼──┐  ┌─┴─┐
    │   mu   │  │ - ◄╌╌T
    └──┬──┬──┘  └─▲─┘
       │  └───────┘
       │
    ┌──▼──┐
    │drain│
    └─────┘

    Output: 123, -123, 123 ...
    """
    oc = OnetimeConstant(123)
    mu = Mu()
    comp = Computation(Operator.NEG)
    drain = Drain()

    w1 = Wire(oc, mu, Input.value_types.DATA)
    oc.add_output(w1)
    mu.add_input(w1)

    ic1 = IntegratedConstant(True, Input.value_types.PREDICATE)
    comp.add_input(ic1)

    w2 = Wire(mu, comp, Input.value_types.DATA)
    mu.add_output(w2)
    comp.add_input(w2)

    w3 = Wire(mu, drain, Input.value_types.DATA)
    mu.add_output(w3)
    drain.add_input(w3)

    w4 = Wire(comp, mu, Input.value_types.DATA)
    comp.add_output(w4)
    mu.add_input(w4)

    return [oc, mu, comp, drain]

def test_Mux():
    """
          ╭───╮  ╭───╮
    ╭───╮ │ T │  │456│ ╭───╮
    │123│ ╰─┬─╯  ╰─┬─╯ │ F │
    ╰───┴┐  ╎      │  ┌┴───╯
       #1│  ╎#1  #2│  ╎#2
         │  ╎      │  ╎
        ┌▼──▼──────▼──▼┐
        │     MUX      │
        └──────┬───────┘
               │
               │
            ┌──▼──┐
            │drain│
            └─────┘

    Output: 123, 123, ...
    """
    cc1 = ContinualConstant(123, name='CC1')
    cc2 = ContinualConstant(True, name='CC2')
    cc3 = ContinualConstant(456, name='CC3')
    cc4 = ContinualConstant(False, name='CC4')
    mux = Mux()
    drain = Drain()

    w1 = Wire(cc1, mux, Input.value_types.DATA, name='PAIR1')

    w2 = Wire(cc2, mux, Input.value_types.PREDICATE, name='PAIR1')

    w3 = Wire(cc3, mux, Input.value_types.DATA, name='PAIR2')

    w4 = Wire(cc4, mux, Input.value_types.PREDICATE, name='PAIR2')

    w5 = Wire(mux, drain, Input.value_types.DATA)

    return [cc1, cc2, cc3, cc4, mux, drain]

def test_MemoryLoad():
    """
    ┌─────┐
     ╲   ╱
      ╲ ╱
       │

    ┌────┐
     ╲  ╱
      ╲╱
       ⎸ ││⎹ ╲|
       │

       │
        ╲
    """

def test_Combine():
    """
          ╔═══╗ ╔═══╗
          ║123║ ║123║
          ╚═══╣ ╠═══╝
          #LHS│ │#RHS
              │ │
    ╔═══╗    ┌▼─▼┐
    ║ T ╟╌╌╌╌► ==│
    ╚═╤═╝    └┬──┘
      ╎       ╎
      ╎       ╎
     ┌▼───────▼┐
     │ combine │
     └────┬────┘
          │
          │
       ┌──▼──┐
       │drain│
       └─────┘

    Output: True
    """

    oc1 = OnetimeConstant(123, name='OC1')
    oc2 = OnetimeConstant(123, name='OC2')
    oc3 = OnetimeConstant(True, name='OC3')
    compare = Computation(Operator.EQ, name='COMP1')
    combine = Combine()
    drain = Drain()

    w1 = Wire(oc1, compare, Input.value_types.DATA, name='LHS')
    w2 = Wire(oc2, compare, Input.value_types.DATA, name='RHS')
    w3 = Wire(oc3, compare, Input.value_types.PREDICATE)
    w4 = Wire(oc3, combine, Input.value_types.PREDICATE)

    w5 = Wire(compare, combine, Input.value_types.PREDICATE)
    w6 = Wire(combine, drain, Input.value_types.DATA)

    return [oc1,oc2,oc3,compare,combine,drain]

def test_trmm_atomic():
    # entry
    e_oc1 = OnetimeConstant(True, name='E_OC1')

    e_oc2 = OnetimeConstant(1, name='E_OC2')
    e_oc3 = OnetimeConstant(0, name='E_OC3') # i
    e_oc4 = OnetimeConstant(0, name='E_OC4') # j

    e_comp1 = Computation(Operator.ADD, name='E_COMP1') # k

    drain1 = Drain(name='DRAIN1')
    drain2 = Drain(name='DRAIN2')
    drain3 = Drain(name='DRAIN3')

    e_w1 = Wire(e_oc2, e_comp1, Input.value_types.DATA, name='RHS')
    e_w2 = Wire(e_oc3, e_comp1, Input.value_types.DATA, name='LHS')

    # for_body
    fb_ml1 = MemoryLoad('n', int, name='FB_ML1')
    fb_comb1 = Combine(name='FB_COMB1')
    fb_comp1 = Computation(Operator.LT, type_=int, name='FB_COMP1')
    fb_comp2 = Computation(Operator.NOT, type_=bool, name='FB_COMP2')
    fb_eta1 = ETA(name='FB_ETA1')
    fb_eta2 = ETA(name='FB_ETA2')

    Wire(fb_ml1, fb_comb1, Input.value_types.PREDICATE)
    Wire(fb_ml1, fb_comp1, Input.value_types.DATA, name='RHS')

    Wire(fb_comb1, fb_eta2, Input.value_types.DATA)
    Wire(fb_comb1, fb_eta1, Input.value_types.DATA)
    Wire(fb_comp1, fb_comp2, Input.value_types.DATA)
    Wire(fb_comp1, fb_eta1, Input.value_types.PREDICATE)
    Wire(fb_comp2, fb_eta2, Input.value_types.PREDICATE)

    # if_else_36
    ie36_cc1 = ContinualConstant(1, name='IE36_CC1')
    ie36_cc2 = ContinualConstant(1, name='IE36_CC2')
    ie36_cc3 = ContinualConstant(0, name='IE36_CC3')
    ie36_comp1 = Computation(Operator.ADD, type_=int, name='IE36_COMP1')
    ie36_comp2 = Computation(Operator.ADD, type_=int, name='IE36_COMP2')
    ie36_eta1 = ETA(name='IE36_ETA1')

    Wire(ie36_cc1, ie36_comp1, Input.value_types.DATA, name='RHS')
    Wire(ie36_comp2, ie36_comp1, Input.value_types.DATA, name='LHS')

    Wire(ie36_cc2, ie36_comp2, Input.value_types.DATA, name='RHS')
    Wire(ie36_cc3, ie36_eta1, Input.value_types.DATA)

    # if_then
    it_ml1 = MemoryLoad('m', int, name='IT_ML1')
    it_comb1 = Combine(name='IT_COMB1')
    it_comp1 = Computation(Operator.LT, type_=int, name='IT_COMP1')
    it_comp2 = Computation(Operator.NOT, type_=int, name='IT_COMP2')
    it_eta1 = ETA(name='IT_ETA1')
    it_eta2 = ETA(name='IT_ETA2')

    Wire(it_ml1, it_comb1, Input.value_types.PREDICATE)
    Wire(it_ml1, it_comp1, Input.value_types.DATA, name='RHS')

    Wire(it_comb1, it_eta1, Input.value_types.DATA)
    Wire(it_comb1, it_eta2, Input.value_types.DATA)

    Wire(it_comp1, it_eta1, Input.value_types.PREDICATE)
    Wire(it_comp1, it_comp2, Input.value_types.DATA)

    Wire(it_comp2, it_eta2, Input.value_types.PREDICATE)

    # if_then12
    it12_cc1 = ContinualConstant(1, name='IT12_CC1')
    it12_comp1 = Computation(Operator.ADD, type_=int, name='IT12_COMP1')
    it12_comp2 = Computation(Operator.MUL, type_=int, name='IT12_COMP2')
    it12_comp3 = Computation(Operator.ADD, type_=int, name='IT12_COMP3')
    it12_eta1 = ETA(name='IT12_ETA1')
    it12_eta2 = ETA(name='IT12_ETA2')
    it12_ml1 = MemoryLoad('A', type_=int, name='IT12_ML1')
    it12_ml2 = MemoryLoad('B', type_=int, name='IT12_ML2')
    it12_ml3 = MemoryLoad('B', type_=int, name='IT12_ML3')
    it12_ms1 = MemoryStore('B', type_=int, name='IT12_MS1')
    it12_comb1 = Combine(name='IT12_COMB1')

    Wire(it12_cc1, it12_comp1, Input.value_types.DATA, name='RHS')

    Wire(it12_ml1, it12_comp2, Input.value_types.DATA, name='LHS')
    Wire(it12_ml1, it12_comb1, Input.value_types.PREDICATE)

    Wire(it12_ml2, it12_comb1, Input.value_types.PREDICATE)
    Wire(it12_ml2, it12_comp2, Input.value_types.DATA, name='RHS')

    Wire(it12_comp2, it12_comp3, Input.value_types.DATA, name='RHS')

    Wire(it12_ml3, it12_comp3, Input.value_types.DATA, name='LHS')
    Wire(it12_ml3, it12_comb1, Input.value_types.PREDICATE)

    Wire(it12_comp3, it12_ms1, Input.value_types.DATA)

    Wire(it12_ms1, it12_comb1, Input.value_types.PREDICATE)

    # if_else
    ie_cc1 = ContinualConstant(1, name='IE_CC1')
    ie_cc2 = ContinualConstant(1, name='IE_CC2')
    ie_ml1 = MemoryLoad('alpha', type_=int, name='IE_ML1')
    ie_ml2 = MemoryLoad('B', type_=int, name='IE_ML2')
    ie_eta1 = ETA(name='IE_ETA1')
    ie_comp1 = Computation(Operator.ADD, type_=int, name='IE_COMP1')
    ie_comp2 = Computation(Operator.ADD, type_=int, name='IE_COMP2')
    ie_comp3 = Computation(Operator.MUL, type_=int, name='IE_COMP3')
    ie_ms1 = MemoryStore('B', type_=int, name='IE_MS1')
    ie_comb1 = Combine(name='IE_COMB1')

    Wire(ie_cc1, ie_comp1, Input.value_types.DATA, name='RHS')
    Wire(ie_cc2, ie_comp2, Input.value_types.DATA, name='RHS')

    Wire(ie_ml1, ie_comp3, Input.value_types.DATA, name='LHS')
    Wire(ie_ml1, ie_comb1, Input.value_types.PREDICATE)

    Wire(ie_ml2, ie_comp3, Input.value_types.DATA, name='RHS')
    Wire(ie_ml2, ie_comb1, Input.value_types.PREDICATE)

    Wire(ie_comp3, ie_ms1, Input.value_types.DATA)

    Wire(ie_ms1, ie_comb1, Input.value_types.PREDICATE)

    # final
    f_mu1 = Mu(name='F_MU1')
    f_mu2 = Mu(name='F_MU2')
    f_mu3 = Mu(name='F_MU3')
    f_mu4 = Mu(name='F_MU4')
    f_ms1 = MemoryStore('k', type_=int, name='F_MS1')
    f_ms2 = MemoryStore('i', type_=int, name='F_MS2')
    f_ms3 = MemoryStore('j', type_=int, name='F_MS3')

    Wire(f_mu1, f_ms1, Input.value_types.DATA) # k
    Wire(f_mu2, f_ms2, Input.value_types.DATA) # i
    Wire(f_mu4, f_ms3, Input.value_types.DATA) # j

    Wire(f_mu3, f_ms1, Input.value_types.PREDICATE)
    Wire(f_mu3, f_ms2, Input.value_types.PREDICATE)
    Wire(f_mu3, f_ms3, Input.value_types.PREDICATE)

    ################
    # Global wires #
    ################

    # g -> entry
    Wire(e_oc1, e_comp1, Input.value_types.PREDICATE)

    # g -> for_body
    Wire(e_oc1, fb_ml1, Input.value_types.PREDICATE)
    Wire(e_oc1, fb_comp1, Input.value_types.PREDICATE)
    Wire(e_oc1, fb_comp2, Input.value_types.PREDICATE)

    # entry -> for_body
    Wire(e_oc4, fb_comp1, Input.value_types.DATA, name='LHS')

    # entry -> if_else36
    Wire(e_oc3, ie36_comp2, Input.value_types.DATA, name='LHS')

    # for_body -> if_else36
    Wire(fb_eta2, ie36_comp1, Input.value_types.PREDICATE)
    Wire(fb_eta2, ie36_comp2, Input.value_types.PREDICATE)
    Wire(fb_eta2, ie36_eta1, Input.value_types.PREDICATE)

    # entry -> if_then
    Wire(e_comp1, it_comp1, Input.value_types.DATA, name='LHS')

    # for_body -> if_then
    Wire(fb_eta1, it_ml1, Input.value_types.PREDICATE)
    Wire(fb_eta1, it_comp1, Input.value_types.PREDICATE)
    Wire(fb_eta1, it_comp2, Input.value_types.PREDICATE)

    # entry -> if_then12
    Wire(e_oc3, it12_eta1, Input.value_types.DATA)
    Wire(e_oc3, it12_ml1, Input.value_types.DATA, name='[1]')
    Wire(e_oc3, it12_ml3, Input.value_types.DATA, name='[0]')
    Wire(e_oc3, it12_ms1, Input.value_types.DATA, name='[0]')

    Wire(e_oc4, it12_eta2, Input.value_types.DATA)
    Wire(e_oc4, it12_ml2, Input.value_types.DATA, name='[1]')
    Wire(e_oc4, it12_ml3, Input.value_types.DATA, name='[1]')
    Wire(e_oc4, it12_ms1, Input.value_types.DATA, name='[1]')

    Wire(e_comp1, it12_comp1, Input.value_types.DATA, name='LHS')
    Wire(e_comp1, it12_ml1, Input.value_types.DATA, name='[0]')
    Wire(e_comp1, it12_ml2, Input.value_types.DATA, name='[0]')

    # if_then -> if_then12
    Wire(it_eta1, it12_comp1, Input.value_types.PREDICATE)
    Wire(it_eta1, it12_eta1, Input.value_types.PREDICATE)
    Wire(it_eta1, it12_ml1, Input.value_types.PREDICATE)
    Wire(it_eta1, it12_eta2, Input.value_types.PREDICATE)
    Wire(it_eta1, it12_ml2, Input.value_types.PREDICATE)
    Wire(it_eta1, it12_comp2, Input.value_types.PREDICATE)
    Wire(it_eta1, it12_ml3, Input.value_types.PREDICATE)
    Wire(it_eta1, it12_comp3, Input.value_types.PREDICATE)
    Wire(it_eta1, it12_ms1, Input.value_types.PREDICATE)

    # entry -> if_else
    Wire(e_oc3, ie_ml2, Input.value_types.DATA, name='[0]')
    Wire(e_oc3, ie_eta1, Input.value_types.DATA)
    Wire(e_oc3, ie_comp1, Input.value_types.DATA, name='LHS')
    Wire(e_oc3, ie_ms1, Input.value_types.DATA, name='[0]')

    Wire(e_oc4, ie_ml2, Input.value_types.DATA, name='[1]')
    Wire(e_oc4, ie_comp2, Input.value_types.DATA, name='LHS')
    Wire(e_oc4, ie_ms1, Input.value_types.DATA, name='[1]')

    # if_then -> if_else
    Wire(it_eta2, ie_ml1, Input.value_types.PREDICATE)
    Wire(it_eta2, ie_ml2, Input.value_types.PREDICATE)
    Wire(it_eta2, ie_eta1, Input.value_types.PREDICATE)
    Wire(it_eta2, ie_comp1, Input.value_types.PREDICATE)
    Wire(it_eta2, ie_comp2, Input.value_types.PREDICATE)
    Wire(it_eta2, ie_comp3, Input.value_types.PREDICATE)
    Wire(it_eta2, ie_ms1, Input.value_types.PREDICATE)

    # for_body -> final
    Wire(fb_eta2, f_mu3, Input.value_types.PREDICATE)

    # if_else_36 -> final
    Wire(ie36_comp1, f_mu1, Input.value_types.DATA)
    Wire(ie36_comp2, f_mu2, Input.value_types.DATA)
    Wire(ie36_eta1, f_mu4, Input.value_types.DATA)

    # if_then12 -> final
    Wire(it12_comp1, f_mu1, Input.value_types.DATA)
    Wire(it12_eta1, f_mu2, Input.value_types.DATA)
    Wire(it12_comb1, f_mu3, Input.value_types.PREDICATE)
    Wire(it12_eta2, f_mu4, Input.value_types.DATA)

    # if_else -> final
    Wire(ie_comp1, f_mu1, Input.value_types.DATA)
    Wire(ie_eta1, f_mu2, Input.value_types.DATA)
    Wire(ie_comb1, f_mu3, Input.value_types.PREDICATE)
    Wire(ie_comp2, f_mu4, Input.value_types.DATA)

    return [drain1, drain2, drain3,
            e_oc1, e_oc2, e_oc3, e_oc4, e_comp1,
            fb_ml1, fb_comb1, fb_comp1, fb_comp2, fb_eta1, fb_eta2,
            ie36_cc1, ie36_cc2, ie36_cc3, ie36_comp1, ie36_comp2, ie36_eta1,
            it_ml1, it_comb1, it_comp1, it_comp2, it_eta1, it_eta2,
            it12_cc1, it12_comp1, it12_comp2, it12_comp3, it12_eta1, it12_eta2, it12_ml1, it12_ml2, it12_ml3, it12_ms1, it12_comb1,
            ie_cc1, ie_cc2, ie_ml1, ie_ml2, ie_eta1, ie_comp1, ie_comp2, ie_comp3, ie_ms1, ie_comb1,
            f_mu1, f_mu2, f_mu3, f_mu4, f_ms1, f_ms2, f_ms3]





def test_trmm_speculated():
    # entry
    e_oc1 = OnetimeConstant(True, name='E_OC1')
    e_oc2 = OnetimeConstant(1, name='E_OC2')
    e_oc3 = OnetimeConstant(0, name='E_OC3') # i
    e_oc4 = OnetimeConstant(0, name='E_OC4') # j
    e_comp1 = Computation(Operator.ADD, name='E_COMP1') # k

    drain1 = Drain(name='DRAIN1')
    drain2 = Drain(name='DRAIN2')
    drain3 = Drain(name='DRAIN3')

    e_w1 = Wire(e_oc2, e_comp1, Input.value_types.DATA, name='RHS')
    e_w2 = Wire(e_oc3, e_comp1, Input.value_types.DATA, name='LHS')

    # for_body
    fb_cc1 = ContinualConstant(True, name='FB_CC1')
    fb_ml1 = MemoryLoad('n', int, name='FB_ML1')
    fb_comb1 = Combine(name='FB_COMB1')
    fb_comb2 = Combine(name='FB_COMB2')
    fb_comb3 = Combine(name='FB_COMB3')
    fb_comp1 = Computation(Operator.LT, type_=int, name='FB_COMP1')
    fb_comp2 = Computation(Operator.NOT, type_=bool, name='FB_COMP2')

    Wire(fb_ml1, fb_comb1, Input.value_types.PREDICATE)
    Wire(fb_ml1, fb_comp1, Input.value_types.DATA, name='RHS')

    Wire(fb_comb1, fb_comb3, Input.value_types.DATA)
    Wire(fb_comb1, fb_comb2, Input.value_types.DATA)
    Wire(fb_comp1, fb_comp2, Input.value_types.DATA)
    Wire(fb_comp1, fb_comb2, Input.value_types.DATA)
    Wire(fb_comp2, fb_comb3, Input.value_types.DATA)

    Wire(fb_cc1, fb_comp1, Input.value_types.PREDICATE)
    Wire(fb_cc1, fb_comp2, Input.value_types.PREDICATE)

    # if_else_36
    ie36_cc1 = ContinualConstant(1, name='IE36_CC1')
    ie36_cc2 = ContinualConstant(1, name='IE36_CC2')
    ie36_cc3 = ContinualConstant(0, name='IE36_CC3')
    ie36_cc4 = ContinualConstant(True, name='IE36_CC4')
    ie36_comp1 = Computation(Operator.ADD, type_=int, name='IE36_COMP1')
    ie36_comp2 = Computation(Operator.ADD, type_=int, name='IE36_COMP2')

    Wire(ie36_cc1, ie36_comp1, Input.value_types.DATA, name='RHS')
    Wire(ie36_comp1, ie36_comp2, Input.value_types.DATA, name='LHS')
    Wire(ie36_cc2, ie36_comp2, Input.value_types.DATA, name='RHS')

    Wire(ie36_cc4, ie36_comp1, Input.value_types.PREDICATE)
    Wire(ie36_cc4, ie36_comp2, Input.value_types.PREDICATE)

    # if_then
    it_cc1 = ContinualConstant(True, name='IT_CC1')
    it_ml1 = MemoryLoad('m', int, name='IT_ML1')
    it_comb1 = Combine(name='IT_COMB1')
    it_comb2 = Combine(name='IT_COMB2')
    it_comb3 = Combine(name='IT_COMB3')
    it_comp1 = Computation(Operator.LT, type_=int, name='IT_COMP1')
    it_comp2 = Computation(Operator.NOT, type_=int, name='IT_COMP2')

    Wire(it_ml1, it_comb1, Input.value_types.PREDICATE)
    Wire(it_ml1, it_comp1, Input.value_types.DATA, name='RHS')

    Wire(it_comb1, it_comb2, Input.value_types.DATA)
    Wire(it_comb1, it_comb3, Input.value_types.DATA)

    Wire(it_comp1, it_comb2, Input.value_types.DATA)
    Wire(it_comp1, it_comp2, Input.value_types.DATA)

    Wire(it_comp2, it_comb3, Input.value_types.DATA)

    Wire(it_cc1, it_comp1, Input.value_types.PREDICATE)
    Wire(it_cc1, it_comp2, Input.value_types.PREDICATE)

    # if_then12
    it12_cc1 = ContinualConstant(1, name='IT12_CC1')
    it12_cc2 = ContinualConstant(True, name='IT12_CC2')
    it12_comp1 = Computation(Operator.ADD, type_=int, name='IT12_COMP1')
    it12_comp2 = Computation(Operator.MUL, type_=int, name='IT12_COMP2')
    it12_comp3 = Computation(Operator.ADD, type_=int, name='IT12_COMP3')
    it12_ml1 = MemoryLoad('A', type_=int, name='IT12_ML1')
    it12_ml2 = MemoryLoad('B', type_=int, name='IT12_ML2')
    it12_ml3 = MemoryLoad('B', type_=int, name='IT12_ML3')
    it12_ms1 = MemoryStore('B', type_=int, name='IT12_MS1')
    it12_comb1 = Combine(name='IT12_COMB1')

    Wire(it12_cc1, it12_comp1, Input.value_types.DATA, name='RHS')

    Wire(it12_ml1, it12_comp2, Input.value_types.DATA, name='LHS')
    Wire(it12_ml1, it12_comb1, Input.value_types.PREDICATE)

    Wire(it12_ml2, it12_comb1, Input.value_types.PREDICATE)
    Wire(it12_ml2, it12_comp2, Input.value_types.DATA, name='RHS')

    Wire(it12_comp2, it12_comp3, Input.value_types.DATA, name='RHS')

    Wire(it12_ml3, it12_comp3, Input.value_types.DATA, name='LHS')
    Wire(it12_ml3, it12_comb1, Input.value_types.PREDICATE)

    Wire(it12_comp3, it12_ms1, Input.value_types.DATA)

    Wire(it12_ms1, it12_comb1, Input.value_types.PREDICATE)

    Wire(it12_cc2, it12_comp1, Input.value_types.PREDICATE)
    Wire(it12_cc2, it12_comp2, Input.value_types.PREDICATE)
    Wire(it12_cc2, it12_comp3, Input.value_types.PREDICATE)

    # if_else
    ie_cc1 = ContinualConstant(1, name='IE_CC1')
    ie_cc2 = ContinualConstant(1, name='IE_CC2')
    ie_cc3 = ContinualConstant(True, name='IE_CC3')
    ie_ml1 = MemoryLoad('alpha', type_=int, name='IE_ML1')
    ie_ml2 = MemoryLoad('B', type_=int, name='IE_ML2')
    ie_comp1 = Computation(Operator.ADD, type_=int, name='IE_COMP1')
    ie_comp2 = Computation(Operator.ADD, type_=int, name='IE_COMP2')
    ie_comp3 = Computation(Operator.MUL, type_=int, name='IE_COMP3')
    ie_ms1 = MemoryStore('B', type_=int, name='IE_MS1')
    ie_comb1 = Combine(name='IE_COMB1')

    Wire(ie_cc1, ie_comp1, Input.value_types.DATA, name='RHS')
    Wire(ie_cc2, ie_comp2, Input.value_types.DATA, name='RHS')

    Wire(ie_ml1, ie_comp3, Input.value_types.DATA, name='LHS')
    Wire(ie_ml1, ie_comb1, Input.value_types.PREDICATE)

    Wire(ie_ml2, ie_comp3, Input.value_types.DATA, name='RHS')
    Wire(ie_ml2, ie_comb1, Input.value_types.PREDICATE)

    Wire(ie_comp3, ie_ms1, Input.value_types.DATA)

    Wire(ie_ms1, ie_comb1, Input.value_types.PREDICATE)

    Wire(ie_cc3, ie_comp1, Input.value_types.PREDICATE)
    Wire(ie_cc3, ie_comp2, Input.value_types.PREDICATE)
    Wire(ie_cc3, ie_comp3, Input.value_types.PREDICATE)

    # final
    f_mux1 = Mux(name='F_MUX1')
    f_mux2 = Mux(name='F_MUX2')
    f_mux3 = Mux(name='F_MUX3')
    f_xor1 = XOR(name='F_XOR1')
    f_ms1 = MemoryStore('k', type_=int, name='F_MS1')
    f_ms2 = MemoryStore('i', type_=int, name='F_MS2')
    f_ms3 = MemoryStore('j', type_=int, name='F_MS3')

    Wire(f_mux1, f_ms3, Input.value_types.DATA) # j
    Wire(f_mux2, f_ms2, Input.value_types.DATA) # i
    Wire(f_mux3, f_ms1, Input.value_types.DATA) # k

    Wire(f_xor1, f_ms1, Input.value_types.PREDICATE)
    Wire(f_xor1, f_ms2, Input.value_types.PREDICATE)
    Wire(f_xor1, f_ms3, Input.value_types.PREDICATE)

    ################
    # Global wires #
    ################

    # e_oc3     i
    # e_oc4     j
    # e_comp1   k

    # f_mux2 i
    # f_mux1 j
    # f_mux3 k

    # g -> entry
    Wire(e_oc1, e_comp1, Input.value_types.PREDICATE)

    # g -> for_body
    Wire(e_oc1, fb_ml1, Input.value_types.PREDICATE)
    Wire(e_oc1, fb_comb1, Input.value_types.PREDICATE)

    # entry -> for_body
    Wire(e_oc4, fb_comp1, Input.value_types.DATA, name='LHS')

    # entry -> if_else36
    Wire(e_oc3, ie36_comp1, Input.value_types.DATA, name='LHS')

    # entry -> if_then
    Wire(e_comp1, it_comp1, Input.value_types.DATA, name='LHS')

    # for_body -> if_then
    Wire(fb_comb2, it_ml1, Input.value_types.PREDICATE)
    Wire(fb_comb2, it_comb1, Input.value_types.PREDICATE)

    # entry -> if_then12
    Wire(e_oc3, it12_ml1, Input.value_types.DATA, name='[1]')
    Wire(e_oc3, it12_ml3, Input.value_types.DATA, name='[0]')
    Wire(e_oc3, it12_ms1, Input.value_types.DATA, name='[0]')

    Wire(e_oc4, it12_ml2, Input.value_types.DATA, name='[1]')
    Wire(e_oc4, it12_ml3, Input.value_types.DATA, name='[1]')
    Wire(e_oc4, it12_ms1, Input.value_types.DATA, name='[1]')

    Wire(e_comp1, it12_ml1, Input.value_types.DATA, name='[0]')
    Wire(e_comp1, it12_ml2, Input.value_types.DATA, name='[0]')
    Wire(e_comp1, it12_comp1, Input.value_types.DATA, name='LHS')

    # if_then -> if_then12
    Wire(it_comb2, it12_ml1, Input.value_types.PREDICATE)
    Wire(it_comb2, it12_ml2, Input.value_types.PREDICATE)
    Wire(it_comb2, it12_ml3, Input.value_types.PREDICATE)
    Wire(it_comb2, it12_ms1, Input.value_types.PREDICATE)
    Wire(it_comb2, it12_comb1, Input.value_types.PREDICATE)

    # entry -> if_else
    Wire(e_oc3, ie_ml2, Input.value_types.DATA, name='[0]')
    Wire(e_oc3, ie_comp1, Input.value_types.DATA, name='LHS')
    Wire(e_oc3, ie_ms1, Input.value_types.DATA, name='[0]')

    Wire(e_oc4, ie_ml2, Input.value_types.DATA, name='[1]')
    Wire(e_oc4, ie_comp2, Input.value_types.DATA, name='LHS')
    Wire(e_oc4, ie_ms1, Input.value_types.DATA, name='[1]')

    # if_then -> if_else
    Wire(it_comb3, ie_ml1, Input.value_types.PREDICATE)
    Wire(it_comb3, ie_ml2, Input.value_types.PREDICATE)
    Wire(it_comb3, ie_ms1, Input.value_types.PREDICATE)
    Wire(it_comb3, ie_comb1, Input.value_types.PREDICATE)

    # for_body -> final
    Wire(fb_comb3, f_xor1, Input.value_types.PREDICATE)
    Wire(fb_comb3, f_mux2, Input.value_types.PREDICATE, name='i1')
    Wire(fb_comb3, f_mux1, Input.value_types.PREDICATE, name='j1')
    Wire(fb_comb3, f_mux3, Input.value_types.PREDICATE, name='k1')

    # if_else_36 -> final
    Wire(ie36_comp1, f_mux2, Input.value_types.DATA, name='i1')
    Wire(ie36_cc3, f_mux1, Input.value_types.DATA, name='j1')
    Wire(ie36_comp2, f_mux3, Input.value_types.DATA, name='k1')

    # if_then12 -> final
    Wire(e_oc3, f_mux2, Input.value_types.DATA, name='i2')
    Wire(e_oc4, f_mux1, Input.value_types.DATA, name='j2')
    Wire(it12_comp1, f_mux3, Input.value_types.DATA, name='k2')

    Wire(it12_comb1, f_xor1, Input.value_types.PREDICATE)
    Wire(it12_comb1, f_mux2, Input.value_types.PREDICATE, name='i2')
    Wire(it12_comb1, f_mux1, Input.value_types.PREDICATE, name='j2')
    Wire(it12_comb1, f_mux3, Input.value_types.PREDICATE, name='k2')

    # if_else -> final
    Wire(e_oc3, f_mux2, Input.value_types.DATA, name='i3')
    Wire(ie_comp2, f_mux1, Input.value_types.DATA, name='j3')
    Wire(ie_comp1, f_mux3, Input.value_types.DATA, name='k3')

    Wire(ie_comb1, f_xor1, Input.value_types.PREDICATE)
    Wire(ie_comb1, f_mux2, Input.value_types.PREDICATE, name='i3')
    Wire(ie_comb1, f_mux1, Input.value_types.PREDICATE, name='j3')
    Wire(ie_comb1, f_mux3, Input.value_types.PREDICATE, name='k3')

    return [drain1, drain2, drain3,
            e_oc1, e_oc2, e_oc3, e_oc4, e_comp1,
            fb_cc1, fb_ml1, fb_comb1, fb_comb2, fb_comb3, fb_comp1, fb_comp2,
            ie36_cc1, ie36_cc2, ie36_cc3, ie36_cc4, ie36_comp1, ie36_comp2,
            it_cc1, it_ml1, it_comb1, it_comb2, it_comb3, it_comp1, it_comp2,
            it12_cc1, it12_cc2, it12_comp1, it12_comp2, it12_comp3, it12_ml1, it12_ml2, it12_ml3, it12_ms1, it12_comb1,
            ie_cc1, ie_cc2, ie_cc3, ie_ml1, ie_ml2, ie_comp1, ie_comp2, ie_comp3, ie_ms1, ie_comb1,
            f_mux1, f_mux2, f_mux3, f_xor1, f_ms1, f_ms2, f_ms3]


def test_trmm_reference():
    # 'mem' variables:
    m = 2
    n = -2
    alpha = 2
    A = [[1,2], [3,4]]
    B = [[5,6], [7,8]]

    # 'normal' variables
    i = 0
    j = 0
    k = i + 1

    if j < n:
        if k < m:
            B[i][j] += A[k][i] * B[k][j]
            k += 1
        else:
            B[i][j] = alpha * B[i][j]
            j += 1
            k = i + 1
    else:
        i += 1
        j = 0
        k = i + 1

    print('A:', A)
    print('B:', B)
    print('i:', i)
    print('j:', j)
    print('k:', k)



# graph = test_monary()
# graph = test_binary()
# graph = test_multiplecomps()
# graph = test_binaryintegrated()
# graph = test_binaryonetime()
# graph = test_ETA()
# graph = test_Mu()
# graph = test_Mux()
# graph = test_Combine()
# graph = test_trmm_atomic()
graph = test_trmm_speculated()
logger = Logger()
mem = DefaultMemorySimulator()

sim = Simulation(graph=graph, mem=mem, logger=logger)

sim.mem.store(-2, 'n')
sim.mem.store(2, 'm')
sim.mem.store(2, 'alpha')
sim.mem.store(30, 'A', [0,0])
sim.mem.store(40, 'A', [0,1])
sim.mem.store(50, 'A', [1,0])
sim.mem.store(60, 'A', [1,1])
sim.mem.store(3, 'B', [0,0])
sim.mem.store(4, 'B', [0,1])
sim.mem.store(5, 'B', [1,0])
sim.mem.store(6, 'B', [1,1])

sim.run()

sim.mem.dump()


print('Reference:')
test_trmm_reference()