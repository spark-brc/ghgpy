# -*- coding: utf-8 -*-
"""
Copyright 2023 by Seonggyu Park 
This file is part of SWAT+GHG tool.
:author: Seonggyu Park
This module contains a framework to summarize the total CH4 flux balance from rice paddy. 
T_{CH4}=P_{CH4}-O_{CH4}+E_{CH4}+D_{CH4}+A_{CH4}

"""

from models import DCmodel
from utils import ObjFns
from utils import PostPr
import pandas as pd
import os
from analyzer import plot_oom
from runs import dc_multi_run






def run_md_viz(wd):
    # run model
    dc_multi_run(wd)
    # post-processing
    m1 = PostPr(wd)
    so_df = m1.get_ch4_so_df()
    print(so_df)

    # viz
    plot_oom(so_df)
    




if __name__ == "__main__":
    wd = "D:\\Projects\\Models\\swatp-ghg\\models"
    run_md_viz(wd)

