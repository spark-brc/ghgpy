from models import DCmodel
import os
import pandas as pd


SFMT = lambda x: "{0:<10s} ".format(str(x))
IFMT = lambda x: "{0:<10d} ".format(int(x))
FFMT = lambda x: "{0:<15.10E} ".format(float(x))




def dc_single_run(wd):
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



def dc_multi_run(wd):
    m1 = DCmodel(wd)
    # read inputs
    sand_cont = 0.8
    root_c_prod = 500
    aglivc = 500 # the amount of above-ground live C for the crop as simulated by DayCent (g C m−2)
    bglivc = 500 # the amount of fine root C for the crop as simulated by DayCent (g C m−2)
    #---------------
    indf = m1.read_inputs()
    indf.dropna(axis=0, inplace=True)
    conts = indf["condition"].unique()
    dff = pd.DataFrame()

    for cont in conts:
        contdf = indf.loc[indf["condition"]==cont]
        ch4prods = []
        ch4eps = []
        ch4ebls = []
        for i in contdf.index:
            # print(contdf.loc[i])
            # calculate CH4 production
            ch4prod = m1.ch4prod(
                sand_cont, float(contdf.loc[i, "eh"]), 
                float(contdf.loc[i, "tsoil"]), root_c_prod)
            ch4prods.append(ch4prod)
            # calculate CH4 emission by plant
            fp = m1.fp(aglivc)
            ch4ep = m1.ch4ep(fp, ch4prod)
            ch4eps.append(ch4ep)
            # calculate CH4 emission by ebullision
            ch4ebl = m1.ch4ebl(
                float(contdf.loc[i, "tsoil"]), ch4prod, ch4ep, bglivc)
            ch4ebls.append(ch4ebl)

        getdf = pd.DataFrame(
            {"ch4prods":ch4prods, "ch4eps":ch4eps, "ch4ebls":ch4ebls}, 
            index=contdf.index)
        getdf["ch4e_tot"] = getdf["ch4eps"] + getdf["ch4ebls"]
        getdf['cont'] = cont
        getdf["ch4_obd"] = contdf.loc[:, "ch4_obd"]
        dff = pd.concat([dff, getdf], axis=0)
    dff.insert(0, "date", dff.index.date)         
    with open(os.path.join(wd, "ch4_multi.out"), "w") as f:
        fmts = [SFMT, FFMT, FFMT, FFMT, FFMT, FFMT, SFMT] 
        f.write("# created by swatp-ghg\n")
        f.write(dff.loc[:, [
            "date", "ch4_obd", "ch4prods", "ch4eps", "ch4ebls", "ch4e_tot", "cont"]].to_string(
                                                        col_space=0,
                                                        formatters=fmts,
                                                        index=False,
                                                        header=True,
                                                        justify="left"))

    # outdf.index = outdf.index.strftime("%Y-%m-%d")

