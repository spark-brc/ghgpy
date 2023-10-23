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
import pandas as pd
import os
from analyzer import plot_one_one, plot_oom


SFMT = lambda x: "{0:<10s} ".format(str(x))
IFMT = lambda x: "{0:<10d} ".format(int(x))
FFMT = lambda x: "{0:<15.10E} ".format(float(x))


def run(wd):
    m1 = DCmodel(wd)
    sand_cont = 0.3
    root_c_prod = 6

    indf = m1.read_inputs()
    indf.dropna(axis=0, inplace=True)

    outdf = pd.DataFrame(
        columns=['ch4prod','ch4ep','ch4ebl'],
        index=indf.index)
    outdf.index.name = "date"
    # outdf.index = outdf.index.strftime("%Y-%m-%d")

    for i in indf.index:
        print(indf.loc[i])
        ch4prod = m1.ch4prod(
            sand_cont, float(indf.loc[i, "eh"]), 
            float(indf.loc[i, "tsoil"]), root_c_prod)
        outdf.loc[i, "ch4prod"] = ch4prod
    outdf.to_csv(os.path.join(wd,"ch4_output.csv"))


def run_multi_cont(wd):
    m1 = DCmodel(wd)
    sand_cont = 0.3
    root_c_prod = 3
    indf = m1.read_inputs()
    indf.dropna(axis=0, inplace=True)
    conts = indf["condition"].unique()
    dff = pd.DataFrame()
    for cont in conts:
        contdf = indf.loc[indf["condition"]==cont]
        ch4prods = []
        for i in contdf.index:
            # print(contdf.loc[i])
            ch4prod = m1.ch4prod(
                sand_cont, float(contdf.loc[i, "eh"]), 
                float(contdf.loc[i, "tsoil"]), root_c_prod)
            ch4prods.append(ch4prod)
        getdf = pd.DataFrame({"ch4prod":ch4prods}, index=contdf.index)
        getdf['cont'] = cont
        dff = pd.concat([dff, getdf], axis=0)
    dff.insert(0, "date", dff.index.date)         
    with open(os.path.join(wd, "ch4_multi.out"), "w") as f:
        f.write("# created by swatp-ghg\n")
        f.write(dff.loc[:, ["date", "ch4prod", "cont"]].to_string(
                                                        col_space=0,
                                                        formatters=[SFMT, FFMT, SFMT],
                                                        index=False,
                                                        header=True,
                                                        justify="left"))

    # outdf.index = outdf.index.strftime("%Y-%m-%d")

def viz(wd):
    m1 = DCmodel(wd)
    obd =  m1.read_inputs()
    obd["date"] = obd.index
    obd["new_idx"] = obd.loc[:, "date"].astype(str) + "-"+ obd.loc[:, "condition"]
    # sim = pd.read_csv(
    #     os.path.join(wd, "ch4_output.csv"), index_col=0, parse_dates=True,)
    simm = pd.read_csv(
        os.path.join(wd, "ch4_multi.out"), sep=r"\s+", comment="#")
    simm["new_idx"] = simm.loc[:, "date"] + "-"+ simm.loc[:, "cont"]
    so_df = simm.merge(obd, how='inner', on='new_idx')

    # print(obd)
    # print(simm)
    # so_df = pd.concat([simm.ch4prod, obd.ch4_obd], axis=1).dropna(axis=0)
    os.chdir(wd)
    # plot_one_one(so_df)
    plot_oom(so_df)

    print(so_df)

    # return so_df





    # print(outdf.loc["2022-06-03", "ch4_obd"])

    # for i in [31,32,33,34,35,36,37,38,39]:
    #     print(m1.ch4prod(eh_init, sand_cont, i, 1))
    # outdf.to_csv(wd, "ch4_output.csv")




if __name__ == "__main__":
    wd = "D:\\Projects\\Models\\swatp-ghg\\models"
    run_multi_cont(wd)
    viz(wd)
    # run_multi_cont(wd)
    # so_df = vis(wd)
    

    # import os
    # wd = "D:\\Projects\\Models\\swatp-ghg\\models"
    # input_df = pd.read_csv(
    #     os.path.join(wd, "input_ghg.csv")
    #     # index_col=0, parse_dates=True
    #     )
    
    # print(input_df.loc["6/3/2022", "eh"])




# class swatpghg(object):

#     def __init__(self, model_dir):
#         self.model_dir = model_dir
#         pass


#     def tot_ch4_flux(y_w):
#         """
#         .. P_{CH4}: CH4 production from soil organic matter with root inputs decomposition and 
#         root exudation after the effects of the electron acceptors have been considered.
#         .. O_{CH4}: CH4 oxidation
#         .. E_{CH4}: CH4 flux from ebullition
#         .. D_{CH4}: CH4 flux from diffusion
#         .. A_{CH4}: CH4 flux from aerenchyma (rice plant)
#         """
#         e_ch4 = Ebullition.e_ch4(y_w) + Diffusion.d_ch4()

#         # tch4 = 

#     def ch4_prod(self, c_soil, f_t, f_Ef, c_root):
#         ch4_prod = conv_fac * f_Ef * (c_soil * f_t * c_root)


