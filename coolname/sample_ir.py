from nodes import *

# Triangular matrix multiplication IR graphs for atomic and speculative
# mode of execution. Should be similar to the DOT representation in /data.

def test_trmm_atomic():
    # entry
    e_oc1 = OnetimeConstant(True, name='E_OC1')

    e_oc2 = OnetimeConstant(1, name='E_OC2')
    e_oc3 = OnetimeConstant(0, name='E_OC3') # i
    e_oc4 = OnetimeConstant(0, name='E_OC4') # j

    e_comp1 = Computation(Operator.ADD, name='E_COMP1') # k

    e_w1 = Wire(e_oc2, e_comp1, Input.value_types.DATA, name='RHS')
    e_w2 = Wire(e_oc3, e_comp1, Input.value_types.DATA, name='LHS')

    # for_body
    fb_ml1 = MemoryLoad('n', int, name='FB_ML1')
    fb_comb1 = Combine(name='FB_COMB1')
    fb_comp1 = Computation(Operator.LT, type_=int, name='FB_COMP1')
    fb_comp2 = Computation(Operator.NOT, type_=bool, name='FB_COMP2')
    fb_eta1 = ETA(name='FB_ETA1')
    fb_eta2 = ETA(name='FB_ETA2')

    fb_w1 = Wire(fb_ml1, fb_comb1, Input.value_types.PREDICATE)
    fb_w2 = Wire(fb_ml1, fb_comp1, Input.value_types.DATA, name='RHS')

    fb_w3 = Wire(fb_comb1, fb_eta2, Input.value_types.DATA)
    fb_w4 = Wire(fb_comb1, fb_eta1, Input.value_types.DATA)
    fb_w5 = Wire(fb_comp1, fb_comp2, Input.value_types.DATA)
    fb_w6 = Wire(fb_comp1, fb_eta1, Input.value_types.PREDICATE)
    fb_w7 = Wire(fb_comp2, fb_eta2, Input.value_types.PREDICATE)

    # if_else_36
    ie36_cc1 = ContinualConstant(1, name='IE36_CC1')
    ie36_cc2 = ContinualConstant(1, name='IE36_CC2')
    ie36_cc3 = ContinualConstant(0, name='IE36_CC3')
    ie36_comp1 = Computation(Operator.ADD, type_=int, name='IE36_COMP1')
    ie36_comp2 = Computation(Operator.ADD, type_=int, name='IE36_COMP2')
    ie36_eta1 = ETA(name='IE36_ETA1')

    ie36_w1 = Wire(ie36_cc1, ie36_comp1, Input.value_types.DATA, name='RHS')
    ie36_w2 = Wire(ie36_comp2, ie36_comp1, Input.value_types.DATA, name='LHS')

    ie36_w3 = Wire(ie36_cc2, ie36_comp2, Input.value_types.DATA, name='RHS')
    ie36_w4 = Wire(ie36_cc3, ie36_eta1, Input.value_types.DATA)

    # if_then
    it_ml1 = MemoryLoad('m', int, name='IT_ML1')
    it_comb1 = Combine(name='IT_COMB1')
    it_comp1 = Computation(Operator.LT, type_=int, name='IT_COMP1')
    it_comp2 = Computation(Operator.NOT, type_=int, name='IT_COMP2')
    it_eta1 = ETA(name='IT_ETA1')
    it_eta2 = ETA(name='IT_ETA2')

    it_w1 = Wire(it_ml1, it_comb1, Input.value_types.PREDICATE)
    it_w2 = Wire(it_ml1, it_comp1, Input.value_types.DATA, name='RHS')

    it_w3 = Wire(it_comb1, it_eta1, Input.value_types.DATA)
    it_w4 = Wire(it_comb1, it_eta2, Input.value_types.DATA)

    it_w5 = Wire(it_comp1, it_eta1, Input.value_types.PREDICATE)
    it_w6 = Wire(it_comp1, it_comp2, Input.value_types.DATA)

    it_w7 = Wire(it_comp2, it_eta2, Input.value_types.PREDICATE)

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

    it12_w1 = Wire(it12_cc1, it12_comp1, Input.value_types.DATA, name='RHS')

    it12_w2 = Wire(it12_ml1, it12_comp2, Input.value_types.DATA, name='LHS')
    it12_w3 = Wire(it12_ml1, it12_comb1, Input.value_types.PREDICATE)

    it12_w4 = Wire(it12_ml2, it12_comb1, Input.value_types.PREDICATE)
    it12_w5 = Wire(it12_ml2, it12_comp2, Input.value_types.DATA, name='RHS')

    it12_w6 = Wire(it12_comp2, it12_comp3, Input.value_types.DATA, name='RHS')

    it12_w7 = Wire(it12_ml3, it12_comp3, Input.value_types.DATA, name='LHS')
    it12_w8 = Wire(it12_ml3, it12_comb1, Input.value_types.PREDICATE)

    it12_w9 = Wire(it12_comp3, it12_ms1, Input.value_types.DATA)

    it12_w10 = Wire(it12_ms1, it12_comb1, Input.value_types.PREDICATE)

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

    ie_w1 = Wire(ie_cc1, ie_comp1, Input.value_types.DATA, name='RHS')
    ie_w2 = Wire(ie_cc2, ie_comp2, Input.value_types.DATA, name='RHS')

    ie_w3 = Wire(ie_ml1, ie_comp3, Input.value_types.DATA, name='LHS')
    ie_w4 = Wire(ie_ml1, ie_comb1, Input.value_types.PREDICATE)

    ie_w5 = Wire(ie_ml2, ie_comp3, Input.value_types.DATA, name='RHS')
    ie_w6 = Wire(ie_ml2, ie_comb1, Input.value_types.PREDICATE)

    ie_w7 = Wire(ie_comp3, ie_ms1, Input.value_types.DATA)

    ie_w8 = Wire(ie_ms1, ie_comb1, Input.value_types.PREDICATE)

    # final
    f_mu1 = Mu(name='F_MU1')
    f_mu2 = Mu(name='F_MU2')
    f_mu3 = Mu(name='F_MU3')
    f_mu4 = Mu(name='F_MU4')
    f_ms1 = MemoryStore('k', type_=int, name='F_MS1')
    f_ms2 = MemoryStore('i', type_=int, name='F_MS2')
    f_ms3 = MemoryStore('j', type_=int, name='F_MS3')

    f_w1 = Wire(f_mu1, f_ms1, Input.value_types.DATA) # k
    f_w2 = Wire(f_mu2, f_ms2, Input.value_types.DATA) # i
    f_w3 = Wire(f_mu4, f_ms3, Input.value_types.DATA) # j

    f_w4 = Wire(f_mu3, f_ms1, Input.value_types.PREDICATE)
    f_w5 = Wire(f_mu3, f_ms2, Input.value_types.PREDICATE)
    f_w6 = Wire(f_mu3, f_ms3, Input.value_types.PREDICATE)

    ################
    # Global wires #
    ################

    # g -> entry
    g_w1 = Wire(e_oc1, e_comp1, Input.value_types.PREDICATE)

    # g -> for_body
    g_w2 = Wire(e_oc1, fb_ml1, Input.value_types.PREDICATE)
    g_w3 = Wire(e_oc1, fb_comp1, Input.value_types.PREDICATE)
    g_w4 = Wire(e_oc1, fb_comp2, Input.value_types.PREDICATE)

    # entry -> for_body
    g_w5 = Wire(e_oc4, fb_comp1, Input.value_types.DATA, name='LHS')

    # entry -> if_else36
    g_w6 = Wire(e_oc3, ie36_comp2, Input.value_types.DATA, name='LHS')

    # for_body -> if_else36
    g_w7 = Wire(fb_eta2, ie36_comp1, Input.value_types.PREDICATE)
    g_w8 = Wire(fb_eta2, ie36_comp2, Input.value_types.PREDICATE)
    g_w9 = Wire(fb_eta2, ie36_eta1, Input.value_types.PREDICATE)

    # entry -> if_then
    g_w10 = Wire(e_comp1, it_comp1, Input.value_types.DATA, name='LHS')

    # for_body -> if_then
    g_w11 = Wire(fb_eta1, it_ml1, Input.value_types.PREDICATE)
    g_w12 = Wire(fb_eta1, it_comp1, Input.value_types.PREDICATE)
    g_w13 = Wire(fb_eta1, it_comp2, Input.value_types.PREDICATE)

    # entry -> if_then12
    g_w14 = Wire(e_oc3, it12_eta1, Input.value_types.DATA)
    g_w15 = Wire(e_oc3, it12_ml1, Input.value_types.DATA, name='[1]')
    g_w16 = Wire(e_oc3, it12_ml3, Input.value_types.DATA, name='[0]')
    g_w17 = Wire(e_oc3, it12_ms1, Input.value_types.DATA, name='[0]')

    g_w18 = Wire(e_oc4, it12_eta2, Input.value_types.DATA)
    g_w19 = Wire(e_oc4, it12_ml2, Input.value_types.DATA, name='[1]')
    g_w20 = Wire(e_oc4, it12_ml3, Input.value_types.DATA, name='[1]')
    g_w21 = Wire(e_oc4, it12_ms1, Input.value_types.DATA, name='[1]')

    g_w22 = Wire(e_comp1, it12_comp1, Input.value_types.DATA, name='LHS')
    g_w23 = Wire(e_comp1, it12_ml1, Input.value_types.DATA, name='[0]')
    g_w24 = Wire(e_comp1, it12_ml2, Input.value_types.DATA, name='[0]')

    # if_then -> if_then12
    g_w25 = Wire(it_eta1, it12_comp1, Input.value_types.PREDICATE)
    g_w26 = Wire(it_eta1, it12_eta1, Input.value_types.PREDICATE)
    g_w27 = Wire(it_eta1, it12_ml1, Input.value_types.PREDICATE)
    g_w28 = Wire(it_eta1, it12_eta2, Input.value_types.PREDICATE)
    g_w29 = Wire(it_eta1, it12_ml2, Input.value_types.PREDICATE)
    g_w30 = Wire(it_eta1, it12_comp2, Input.value_types.PREDICATE)
    g_w31 = Wire(it_eta1, it12_ml3, Input.value_types.PREDICATE)
    g_w32 = Wire(it_eta1, it12_comp3, Input.value_types.PREDICATE)
    g_w33 = Wire(it_eta1, it12_ms1, Input.value_types.PREDICATE)

    # entry -> if_else
    g_w34 = Wire(e_oc3, ie_ml2, Input.value_types.DATA, name='[0]')
    g_w35 = Wire(e_oc3, ie_eta1, Input.value_types.DATA)
    g_w36 = Wire(e_oc3, ie_comp1, Input.value_types.DATA, name='LHS')
    g_w37 = Wire(e_oc3, ie_ms1, Input.value_types.DATA, name='[0]')

    g_w38 = Wire(e_oc4, ie_ml2, Input.value_types.DATA, name='[1]')
    g_w39 = Wire(e_oc4, ie_comp2, Input.value_types.DATA, name='LHS')
    g_w40 = Wire(e_oc4, ie_ms1, Input.value_types.DATA, name='[1]')

    # if_then -> if_else
    g_w41 = Wire(it_eta2, ie_ml1, Input.value_types.PREDICATE)
    g_w42 = Wire(it_eta2, ie_ml2, Input.value_types.PREDICATE)
    g_w43 = Wire(it_eta2, ie_eta1, Input.value_types.PREDICATE)
    g_w44 = Wire(it_eta2, ie_comp1, Input.value_types.PREDICATE)
    g_w45 = Wire(it_eta2, ie_comp2, Input.value_types.PREDICATE)
    g_w46 = Wire(it_eta2, ie_comp3, Input.value_types.PREDICATE)
    g_w47 = Wire(it_eta2, ie_ms1, Input.value_types.PREDICATE)

    # for_body -> final
    g_w48 = Wire(fb_eta2, f_mu3, Input.value_types.PREDICATE)

    # if_else_36 -> final
    g_w49 = Wire(ie36_comp1, f_mu1, Input.value_types.DATA)
    g_w50 = Wire(ie36_comp2, f_mu2, Input.value_types.DATA)
    g_w51 = Wire(ie36_eta1, f_mu4, Input.value_types.DATA)

    # if_then12 -> final
    g_w52 = Wire(it12_comp1, f_mu1, Input.value_types.DATA)
    g_w53 = Wire(it12_eta1, f_mu2, Input.value_types.DATA)
    g_w54 = Wire(it12_comb1, f_mu3, Input.value_types.PREDICATE)
    g_w55 = Wire(it12_eta2, f_mu4, Input.value_types.DATA)

    # if_else -> final
    g_w56 = Wire(ie_comp1, f_mu1, Input.value_types.DATA)
    g_w57 = Wire(ie_eta1, f_mu2, Input.value_types.DATA)
    g_w58 = Wire(ie_comb1, f_mu3, Input.value_types.PREDICATE)
    g_w59 = Wire(ie_comp2, f_mu4, Input.value_types.DATA)

    return IR([[e_oc1],
            [e_oc2, e_oc3, e_oc4, e_comp1],
            [fb_ml1, fb_comb1, fb_comp1, fb_comp2, fb_eta1, fb_eta2],
            [ie36_cc1, ie36_cc2, ie36_cc3, ie36_comp1, ie36_comp2, ie36_eta1],
            [it_ml1, it_comb1, it_comp1, it_comp2, it_eta1, it_eta2],
            [it12_cc1, it12_comp1, it12_comp2, it12_comp3, it12_eta1, it12_eta2, it12_ml1, it12_ml2, it12_ml3, it12_ms1, it12_comb1],
            [ie_cc1, ie_cc2, ie_ml1, ie_ml2, ie_eta1, ie_comp1, ie_comp2, ie_comp3, ie_ms1, ie_comb1],
            [f_mu1, f_mu2, f_mu3, f_mu4, f_ms1, f_ms2, f_ms3]],
           [e_w1, e_w2,
            fb_w1, fb_w2, fb_w3, fb_w4, fb_w5, fb_w6, fb_w7,
            ie36_w1, ie36_w2, ie36_w3, ie36_w4,
            it_w1, it_w2, it_w3, it_w4, it_w5, it_w6, it_w7,
            it12_w1, it12_w2, it12_w3, it12_w4, it12_w5, it12_w6, it12_w7, it12_w8, it12_w9, it12_w10,
            ie_w1, ie_w2, ie_w3, ie_w4, ie_w5, ie_w6, ie_w7, ie_w8,
            f_w1, f_w2, f_w3, f_w4, f_w5, f_w6,
            g_w1, g_w2, g_w3, g_w4, g_w5, g_w6, g_w7, g_w8, g_w9, g_w10, g_w11, g_w12, g_w13, g_w14, g_w15, g_w16, g_w17, g_w18, g_w19, g_w20, g_w21, g_w22, g_w23, g_w24, g_w25, g_w26, g_w27, g_w28, g_w29, g_w30, g_w31, g_w32, g_w33, g_w34, g_w35, g_w36, g_w37, g_w38, g_w39, g_w40, g_w41, g_w42, g_w43, g_w44, g_w45, g_w46, g_w47, g_w48, g_w49, g_w50, g_w51, g_w52, g_w53,g_w54,g_w55,g_w56,g_w57,g_w58,g_w59])

def test_trmm_speculated():
    # entry
    e_oc1 = OnetimeConstant(True, name='E_OC1')
    e_oc2 = OnetimeConstant(1, name='E_OC2')
    e_oc3 = OnetimeConstant(0, name='E_OC3') # i
    e_oc4 = OnetimeConstant(0, name='E_OC4') # j
    e_comp1 = Computation(Operator.ADD, name='E_COMP1') # k

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

    fb_w1 = Wire(fb_ml1, fb_comb1, Input.value_types.PREDICATE)
    fb_w2 = Wire(fb_ml1, fb_comp1, Input.value_types.DATA, name='RHS')

    fb_w3 = Wire(fb_comb1, fb_comb3, Input.value_types.DATA)
    fb_w4 = Wire(fb_comb1, fb_comb2, Input.value_types.DATA)
    fb_w5 = Wire(fb_comp1, fb_comp2, Input.value_types.DATA)
    fb_w6 = Wire(fb_comp1, fb_comb2, Input.value_types.DATA)
    fb_w7 = Wire(fb_comp2, fb_comb3, Input.value_types.DATA)

    fb_w8 = Wire(fb_cc1, fb_comp1, Input.value_types.PREDICATE)
    fb_w9 = Wire(fb_cc1, fb_comp2, Input.value_types.PREDICATE)

    # if_else_36
    ie36_cc1 = ContinualConstant(1, name='IE36_CC1')
    ie36_cc2 = ContinualConstant(1, name='IE36_CC2')
    ie36_cc3 = ContinualConstant(0, name='IE36_CC3')
    ie36_cc4 = ContinualConstant(True, name='IE36_CC4')
    ie36_comp1 = Computation(Operator.ADD, type_=int, name='IE36_COMP1')
    ie36_comp2 = Computation(Operator.ADD, type_=int, name='IE36_COMP2')

    ie36_w1 = Wire(ie36_cc1, ie36_comp1, Input.value_types.DATA, name='RHS')
    ie36_w2 = Wire(ie36_comp1, ie36_comp2, Input.value_types.DATA, name='LHS')
    ie36_w3 = Wire(ie36_cc2, ie36_comp2, Input.value_types.DATA, name='RHS')

    ie36_w4 = Wire(ie36_cc4, ie36_comp1, Input.value_types.PREDICATE)
    ie36_w5 = Wire(ie36_cc4, ie36_comp2, Input.value_types.PREDICATE)

    # if_then
    it_cc1 = ContinualConstant(True, name='IT_CC1')
    it_ml1 = MemoryLoad('m', int, name='IT_ML1')
    it_comb1 = Combine(name='IT_COMB1')
    it_comb2 = Combine(name='IT_COMB2')
    it_comb3 = Combine(name='IT_COMB3')
    it_comp1 = Computation(Operator.LT, type_=int, name='IT_COMP1')
    it_comp2 = Computation(Operator.NOT, type_=int, name='IT_COMP2')

    it_w1 = Wire(it_ml1, it_comb1, Input.value_types.PREDICATE)
    it_w2 = Wire(it_ml1, it_comp1, Input.value_types.DATA, name='RHS')

    it_w3 = Wire(it_comb1, it_comb2, Input.value_types.DATA)
    it_w4 = Wire(it_comb1, it_comb3, Input.value_types.DATA)

    it_w5 = Wire(it_comp1, it_comb2, Input.value_types.DATA)
    it_w6 = Wire(it_comp1, it_comp2, Input.value_types.DATA)

    it_w7 = Wire(it_comp2, it_comb3, Input.value_types.DATA)

    it_w8 = Wire(it_cc1, it_comp1, Input.value_types.PREDICATE)
    it_w9 = Wire(it_cc1, it_comp2, Input.value_types.PREDICATE)

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

    it12_w1 = Wire(it12_cc1, it12_comp1, Input.value_types.DATA, name='RHS')

    it12_w2 = Wire(it12_ml1, it12_comp2, Input.value_types.DATA, name='LHS')
    it12_w3 = Wire(it12_ml1, it12_comb1, Input.value_types.PREDICATE)

    it12_w4 = Wire(it12_ml2, it12_comb1, Input.value_types.PREDICATE)
    it12_w5 = Wire(it12_ml2, it12_comp2, Input.value_types.DATA, name='RHS')

    it12_w6 = Wire(it12_comp2, it12_comp3, Input.value_types.DATA, name='RHS')

    it12_w7 = Wire(it12_ml3, it12_comp3, Input.value_types.DATA, name='LHS')
    it12_w8 = Wire(it12_ml3, it12_comb1, Input.value_types.PREDICATE)

    it12_w9 = Wire(it12_comp3, it12_ms1, Input.value_types.DATA)

    it12_w10 = Wire(it12_ms1, it12_comb1, Input.value_types.PREDICATE)

    it12_w11 = Wire(it12_cc2, it12_comp1, Input.value_types.PREDICATE)
    it12_w12 = Wire(it12_cc2, it12_comp2, Input.value_types.PREDICATE)
    it12_w13 = Wire(it12_cc2, it12_comp3, Input.value_types.PREDICATE)

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

    ie_w1 = Wire(ie_cc1, ie_comp1, Input.value_types.DATA, name='RHS')
    ie_w2 = Wire(ie_cc2, ie_comp2, Input.value_types.DATA, name='RHS')

    ie_w3 = Wire(ie_ml1, ie_comp3, Input.value_types.DATA, name='LHS')
    ie_w4 = Wire(ie_ml1, ie_comb1, Input.value_types.PREDICATE)

    ie_w5 = Wire(ie_ml2, ie_comp3, Input.value_types.DATA, name='RHS')
    ie_w6 = Wire(ie_ml2, ie_comb1, Input.value_types.PREDICATE)

    ie_w7 = Wire(ie_comp3, ie_ms1, Input.value_types.DATA)

    ie_w8 = Wire(ie_ms1, ie_comb1, Input.value_types.PREDICATE)

    ie_w9 = Wire(ie_cc3, ie_comp1, Input.value_types.PREDICATE)
    ie_w10 = Wire(ie_cc3, ie_comp2, Input.value_types.PREDICATE)
    ie_w11 = Wire(ie_cc3, ie_comp3, Input.value_types.PREDICATE)

    # final
    f_mux1 = Mux(name='F_MUX1')
    f_mux2 = Mux(name='F_MUX2')
    f_mux3 = Mux(name='F_MUX3')
    f_xor1 = XOR(name='F_XOR1')
    f_ms1 = MemoryStore('k', type_=int, name='F_MS1')
    f_ms2 = MemoryStore('i', type_=int, name='F_MS2')
    f_ms3 = MemoryStore('j', type_=int, name='F_MS3')

    f_w1 = Wire(f_mux1, f_ms3, Input.value_types.DATA) # j
    f_w2 = Wire(f_mux2, f_ms2, Input.value_types.DATA) # i
    f_w3 = Wire(f_mux3, f_ms1, Input.value_types.DATA) # k

    f_w4 = Wire(f_xor1, f_ms1, Input.value_types.PREDICATE)
    f_w5 = Wire(f_xor1, f_ms2, Input.value_types.PREDICATE)
    f_w6 = Wire(f_xor1, f_ms3, Input.value_types.PREDICATE)

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
    g_w1 = Wire(e_oc1, e_comp1, Input.value_types.PREDICATE)

    # g -> for_body
    g_w2 = Wire(e_oc1, fb_ml1, Input.value_types.PREDICATE)
    g_w3 = Wire(e_oc1, fb_comb1, Input.value_types.PREDICATE)

    # entry -> for_body
    g_w4 = Wire(e_oc4, fb_comp1, Input.value_types.DATA, name='LHS')

    # entry -> if_else36
    g_w5 = Wire(e_oc3, ie36_comp1, Input.value_types.DATA, name='LHS')

    # entry -> if_then
    g_w6 = Wire(e_comp1, it_comp1, Input.value_types.DATA, name='LHS')

    # for_body -> if_then
    g_w7 = Wire(fb_comb2, it_ml1, Input.value_types.PREDICATE)
    g_w8 = Wire(fb_comb2, it_comb1, Input.value_types.PREDICATE)

    # entry -> if_then12
    g_w9 = Wire(e_oc3, it12_ml1, Input.value_types.DATA, name='[1]')
    g_w10 = Wire(e_oc3, it12_ml3, Input.value_types.DATA, name='[0]')
    g_w11 = Wire(e_oc3, it12_ms1, Input.value_types.DATA, name='[0]')

    g_w12 = Wire(e_oc4, it12_ml2, Input.value_types.DATA, name='[1]')
    g_w13 = Wire(e_oc4, it12_ml3, Input.value_types.DATA, name='[1]')
    g_w14 = Wire(e_oc4, it12_ms1, Input.value_types.DATA, name='[1]')

    g_w15 = Wire(e_comp1, it12_ml1, Input.value_types.DATA, name='[0]')
    g_w16 = Wire(e_comp1, it12_ml2, Input.value_types.DATA, name='[0]')
    g_w17 = Wire(e_comp1, it12_comp1, Input.value_types.DATA, name='LHS')

    # if_then -> if_then12
    g_w18 = Wire(it_comb2, it12_ml1, Input.value_types.PREDICATE)
    g_w19 = Wire(it_comb2, it12_ml2, Input.value_types.PREDICATE)
    g_w20 = Wire(it_comb2, it12_ml3, Input.value_types.PREDICATE)
    g_w21 = Wire(it_comb2, it12_ms1, Input.value_types.PREDICATE)
    g_w22 = Wire(it_comb2, it12_comb1, Input.value_types.PREDICATE)

    # entry -> if_else
    g_w23 = Wire(e_oc3, ie_ml2, Input.value_types.DATA, name='[0]')
    g_w24 = Wire(e_oc3, ie_comp1, Input.value_types.DATA, name='LHS')
    g_w25 = Wire(e_oc3, ie_ms1, Input.value_types.DATA, name='[0]')

    g_w26 = Wire(e_oc4, ie_ml2, Input.value_types.DATA, name='[1]')
    g_w27 = Wire(e_oc4, ie_comp2, Input.value_types.DATA, name='LHS')
    g_w28 = Wire(e_oc4, ie_ms1, Input.value_types.DATA, name='[1]')

    # if_then -> if_else
    g_w29 = Wire(it_comb3, ie_ml1, Input.value_types.PREDICATE)
    g_w30 = Wire(it_comb3, ie_ml2, Input.value_types.PREDICATE)
    g_w31 = Wire(it_comb3, ie_ms1, Input.value_types.PREDICATE)
    g_w32 = Wire(it_comb3, ie_comb1, Input.value_types.PREDICATE)

    # for_body -> final
    g_w33 = Wire(fb_comb3, f_xor1, Input.value_types.PREDICATE)
    g_w34 = Wire(fb_comb3, f_mux2, Input.value_types.PREDICATE, name='i1')
    g_w35 = Wire(fb_comb3, f_mux1, Input.value_types.PREDICATE, name='j1')
    g_w36 = Wire(fb_comb3, f_mux3, Input.value_types.PREDICATE, name='k1')

    # if_else_36 -> final
    g_w37 = Wire(ie36_comp1, f_mux2, Input.value_types.DATA, name='i1')
    g_w38 = Wire(ie36_cc3, f_mux1, Input.value_types.DATA, name='j1')
    g_w39 = Wire(ie36_comp2, f_mux3, Input.value_types.DATA, name='k1')

    # if_then12 -> final
    g_w40 = Wire(e_oc3, f_mux2, Input.value_types.DATA, name='i2')
    g_w41 = Wire(e_oc4, f_mux1, Input.value_types.DATA, name='j2')
    g_w42 = Wire(it12_comp1, f_mux3, Input.value_types.DATA, name='k2')

    g_w43 = Wire(it12_comb1, f_xor1, Input.value_types.PREDICATE)
    g_w44 = Wire(it12_comb1, f_mux2, Input.value_types.PREDICATE, name='i2')
    g_w45 = Wire(it12_comb1, f_mux1, Input.value_types.PREDICATE, name='j2')
    g_w46 = Wire(it12_comb1, f_mux3, Input.value_types.PREDICATE, name='k2')

    # if_else -> final
    g_w47 = Wire(e_oc3, f_mux2, Input.value_types.DATA, name='i3')
    g_w48 = Wire(ie_comp2, f_mux1, Input.value_types.DATA, name='j3')
    g_w49 = Wire(ie_comp1, f_mux3, Input.value_types.DATA, name='k3')

    g_w50 = Wire(ie_comb1, f_xor1, Input.value_types.PREDICATE)
    g_w51 = Wire(ie_comb1, f_mux2, Input.value_types.PREDICATE, name='i3')
    g_w52 = Wire(ie_comb1, f_mux1, Input.value_types.PREDICATE, name='j3')
    g_w53 = Wire(ie_comb1, f_mux3, Input.value_types.PREDICATE, name='k3')

    return IR([[e_oc1],
                  [e_oc2, e_oc3, e_oc4, e_comp1],
                  [fb_cc1, fb_ml1, fb_comb1, fb_comb2, fb_comb3, fb_comp1, fb_comp2],
                  [ie36_cc1, ie36_cc2, ie36_cc3, ie36_cc4, ie36_comp1, ie36_comp2],
                  [it_cc1, it_ml1, it_comb1, it_comb2, it_comb3, it_comp1, it_comp2],
                  [it12_cc1, it12_cc2, it12_comp1, it12_comp2, it12_comp3, it12_ml1, it12_ml2, it12_ml3, it12_ms1, it12_comb1],
                  [ie_cc1, ie_cc2, ie_cc3, ie_ml1, ie_ml2, ie_comp1, ie_comp2, ie_comp3, ie_ms1, ie_comb1],
                  [f_mux1, f_mux2, f_mux3, f_xor1, f_ms1, f_ms2, f_ms3]],
                 [e_w1, e_w2,
                  fb_w1, fb_w2, fb_w3, fb_w4, fb_w5, fb_w6, fb_w7, fb_w8, fb_w9,
                  ie36_w1, ie36_w2, ie36_w3, ie36_w4, ie36_w5,
                  it_w1, it_w2, it_w3, it_w4, it_w5, it_w6, it_w7, it_w8, it_w9,
                  it12_w1, it12_w2, it12_w3, it12_w4, it12_w5, it12_w6, it12_w7, it12_w8, it12_w9, it12_w10, it12_w11, it12_w12, it12_w13,
                  ie_w1, ie_w2, ie_w3, ie_w4, ie_w5, ie_w6, ie_w7, ie_w8, ie_w9, ie_w10, ie_w11,
                  f_w1, f_w2, f_w3, f_w4, f_w5, f_w6,
                  g_w1, g_w2, g_w3, g_w4, g_w5, g_w6, g_w7, g_w8, g_w9, g_w10, g_w11, g_w12, g_w13, g_w14, g_w15, g_w16, g_w17, g_w18, g_w19, g_w20, g_w21, g_w22, g_w23, g_w24, g_w25, g_w26, g_w27, g_w28, g_w29, g_w30, g_w31, g_w32, g_w33, g_w34, g_w35, g_w36, g_w37, g_w38, g_w39, g_w40, g_w41, g_w42, g_w43, g_w44, g_w45, g_w46, g_w47, g_w48, g_w49, g_w50, g_w51, g_w52, g_w53])