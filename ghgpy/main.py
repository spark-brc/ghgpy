# -*- coding: utf-8 -*-
"""
Copyright 2023 by Seonggyu Park 
This file is part of ghgpy.
:author: Seonggyu Park
This module contains a framework to summarize the total CH4 flux balance from rice paddy. 
:math:`T_{CH4}=P_{CH4}-O_{CH4}+E_{CH4}+D_{CH4}+A_{CH4}`

"""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

from ghgpy.models import DCmodel
from ghgpy.utils import ObjFns
from ghgpy.utils import PostPr
import pandas as pd
import os
from ghgpy.analyzer import plot_oom, plot_tseries_ch4
from ghgpy.runs import run_dc_multi, run_dndc_daily



def run_dndc(wd):
    run_dndc_daily(wd)
    so_df = PostPr(wd).get_ch4_so_df(outfnam="ch4_multi_dndc.out")
    # viz
    plot_tseries_ch4(so_df, simnam="ch4es", height=3, dot=False)


def run_dc(wd):
    run_dc_multi(wd)
    so_df = PostPr(wd).get_ch4_so_df(outfnam="ch4_multi_dc.out")
    plot_tseries_ch4(so_df, height=3, dot=False, fignam="dc_out.png")

def run_md_viz(wd):
    # run model
    run_dc_multi(wd)
    # post-processing
    m1 = PostPr(wd)


    so_df = m1.get_ch4_so_df(outfnam="ch4_multi_dndc.out")
    # so_df = m1.get_ch4_so_df(outfnam="ch4_multi.out")
    print(so_df)

    # viz
    plot_tseries_ch4(so_df, dot=False)
    




if __name__ == "__main__":
    wd = "D:\\Projects\\Tools\\ghgpy\\models"
    run_dc(wd)

