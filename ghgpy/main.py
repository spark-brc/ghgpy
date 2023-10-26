# -*- coding: utf-8 -*-
"""
Copyright 2023 by Seonggyu Park 
This file is part of SWAT+GHG tool.
:author: Seonggyu Park
This module contains a framework to summarize the total CH4 flux balance from rice paddy. 
T_{CH4}=P_{CH4}-O_{CH4}+E_{CH4}+D_{CH4}+A_{CH4}

"""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

from swatp_ghg.models import DCmodel
from swatp_ghg.utils import ObjFns
from swatp_ghg.utils import PostPr
import pandas as pd
import os
from swatp_ghg.analyzer import plot_oom
from swatp_ghg.runs import dc_multi_run






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

