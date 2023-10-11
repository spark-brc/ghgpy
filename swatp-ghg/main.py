# -*- coding: utf-8 -*-
"""
Copyright 2023 by Seonggyu Park 
This file is part of SWAT+GHG tool.
:author: Seonggyu Park
This module contains a framework to summarize the total CH4 flux balance from rice paddy. 
T_{CH4}=P_{CH4}-O_{CH4}+E_{CH4}+D_{CH4}+A_{CH4}

"""

from ch4_process import Decomposition, Ebullition, Diffusion



class swatpghg(object):

    def __init__(self, model_dir):
        self.model_dir = model_dir
        pass


    def tot_ch4_flux(y_w):
        """
        .. P_{CH4}: CH4 production from soil organic matter with root inputs decomposition and 
        root exudation after the effects of the electron acceptors have been considered.
        .. O_{CH4}: CH4 oxidation
        .. E_{CH4}: CH4 flux from ebullition
        .. D_{CH4}: CH4 flux from diffusion
        .. A_{CH4}: CH4 flux from aerenchyma (rice plant)
        """
        e_ch4 = Ebullition.e_ch4(y_w) + Diffusion.d_ch4()

        # tch4 = 

    def ch4_prod(self, c_soil, f_t, f_Ef, c_root):
        ch4_prod = conv_fac * f_Ef * (c_soil * f_t * c_root)


