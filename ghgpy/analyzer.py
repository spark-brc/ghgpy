import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from ghgpy.utils import ObjFns
import numpy as np
import pandas as pd
import os
from ghgpy.models import DCmodel


def plot_oo(df, target=None,numcols=1, fsize=8):
    m1 = ObjFns()
    if target is None:
        target = "ch4e_tot"
    fig, ax = plt.subplots(figsize=(6,5))
    # colors = cm.tab20(np.linspace(0, 1, len(df.site_name.unique())))
    fmax = df.loc[:, ["ch4prods", "ch4_obd"]].max().max()
    fmin = df.loc[:, ["ch4prods", "ch4_obd"]].min().min()
    x_val = df.loc[:, "ch4prods"].tolist()
    y_val = df.loc[:, "ch4_obd"].tolist()
    correlation_matrix = np.corrcoef(x_val, y_val)
    correlation_xy = correlation_matrix[0,1]
    r_squared = correlation_xy**2
    m, b = np.polyfit(x_val, y_val, 1)
    ax.plot(np.array(x_val), (m*np.array(x_val)) + b, 'k', label='_nolegend_')
    ax.text(
            0.05, 0.9,
            f'$R^2:$ {r_squared:.3f}',
            horizontalalignment='left',
            bbox=dict(facecolor='gray', alpha=0.2),
            transform=ax.transAxes
            )
    ax.text(
            0.95, 0.05,
            f'$y={m:.2f}x{b:.2f}$',
            horizontalalignment='right',
            # bbox=dict(facecolor='gray', alpha=0.2),
            transform=ax.transAxes
            )
    ax.scatter(df[target], df.ch4_obd,  alpha=0.7)
    rsq_val = round(m1.rsq(df[target], df.ch4_obd), 3)
    rmse_val = round(m1.rmse(df[target].values, df.ch4_obd.values), 3)
    pbias_val = round(m1.pbias(df[target].values, df.ch4_obd.values), 3)

    # lgds = []
    # for tn, c in zip(df.site_name.unique(), colors):
    #     sdf = df.loc[df['site_name'] == tn]
    #     ax.scatter(
    #         sdf.somsc_sim, sdf.obd, 
    #         color = c, 
    #         alpha=0.7)
    #     rsq_val = round(rsquared(sdf.obd, sdf.somsc_sim), 3)
    #     rmse_val = round(rmse(sdf.obd, sdf.somsc_sim), 3)
    #     lgds.append(f"{tn} (rsq:{rsq_val}, rmse:{rmse_val})")
    ax.plot([fmin, fmax], [fmin, fmax], 'k--', alpha=0.2)
    ax.set_xlabel("Simulated CH4 ($CH4-C$ $m^{-2} d^{-1}$)")
    ax.set_ylabel("Observed CH4 ($CH4-C$ $m^{-2} d^{-1}$)")
    # plt.legend(
    #     lgds, 
    #     bbox_to_anchor=(1.05, 1.05), ncols=numcols, fontsize=fsize)
    # fig.tight_layout()
    plt.savefig("plot_oneToOne.jpg", dpi=300, bbox_inches="tight")
    plt.show()


def plot_oom(df, target=None, obdnam=None, numcols=1, fsize=8):
    # plot one to one multi sites or scenarios
    m1 = ObjFns()
    if target is None:
        target = "ch4e_tot"
    if obdnam is None:
        obdnam = "ch4_obd"
    fig, ax = plt.subplots(figsize=(6,5))
    colors = cm.rainbow(np.linspace(0, 1, len(df.cont.unique())))
    print(df)
    fmax = df.loc[:, [target, obdnam]].max().max()
    fmin = df.loc[:, [target, obdnam]].min().min()
    x_val = df.loc[:, target].tolist()
    y_val = df.loc[:, obdnam].tolist()
    correlation_matrix = np.corrcoef(x_val, y_val)
    correlation_xy = correlation_matrix[0,1]
    r_squared = correlation_xy**2

    m, b = np.polyfit(x_val, y_val, 1)
    ax.plot(np.array(x_val), (m*np.array(x_val)) + b, 'k', label='_nolegend_')
    
    rsq_val = round(m1.rsq(df[target], df.ch4_obd), 3)
    rmse_val = round(m1.rmse(df[target].values, df.ch4_obd.values), 3)
    pbias_val = round(m1.pbias(df[target].values, df.ch4_obd.values), 3)
    ax.text(
            0.05, 0.9,
            f'$R^2:$ {r_squared:.3f}',
            horizontalalignment='left',
            bbox=dict(facecolor='gray', alpha=0.2),
            transform=ax.transAxes
            )
    ax.text(
            0.3, 0.9,
            f'$R^2:$2 {rsq_val:.3f}',
            horizontalalignment='left',
            bbox=dict(facecolor='gray', alpha=0.2),
            transform=ax.transAxes
            )
    ax.text(
            0.7, 0.9,
            f'$rmse:$ {rmse_val:.3f}',
            horizontalalignment='left',
            bbox=dict(facecolor='gray', alpha=0.2),
            transform=ax.transAxes
            )
    ax.text(
            0.95, 0.05,
            f'$y={m:.2f}x{b:.2f}$',
            horizontalalignment='right',
            # bbox=dict(facecolor='gray', alpha=0.2),
            transform=ax.transAxes
            )
    # ax.scatter(df[target], df.ch4_obd,  alpha=0.7)
    lgds = []
    for tn, c in zip(df.cont.unique(), colors):
        sdf = df.loc[df['cont'] == tn]
        ax.scatter(
            sdf[target], sdf.ch4_obd, 
            color = c, 
            alpha=0.7)
        rsq_val = round(m1.rsq(sdf[target], sdf.ch4_obd), 3)
        rmse_val = round(m1.rmse(sdf[target].values, sdf.ch4_obd.values), 3)
        lgds.append(f"{tn} (rsq:{rsq_val}, rmse:{rmse_val})")
    ax.plot([fmin, fmax], [fmin, fmax], 'k--', alpha=0.2)
    ax.set_xlabel("Simulated CH4 ($CH4-C$ $m^{-2} d^{-1}$)")
    ax.set_ylabel("Observed CH4 ($CH4-C$ $m^{-2} d^{-1}$)")
    plt.legend(
        lgds, 
        # bbox_to_anchor=(1.05, 1.1),
        ncols=numcols, fontsize=fsize
        )
    fig.tight_layout()
    plt.savefig("plot_oom.jpg", dpi=300, bbox_inches="tight")
    plt.show()


# def plot_tseries_ch4(
#                     df, target=None, obdnam=None, width=10, height=4, dot=True,
#                     ):
#     if target is None:
#         target = "ch4e_tot"
#     if obdnam is None:
#         obdnam = "ch4_obd"

#     fig, ax = plt.subplots()


#     obs = pst.observation_data.copy()
#     obs = obs.loc[obs.obgnme.apply(lambda x: x in pst.nnz_obs_groups),:]
#     time_col = []
#     for i in range(len(obs)):
#         time_col.append(obs.iloc[i, 0][-6:])
#     obs['time'] = time_col
# #     # onames provided in oname argument
# #     obs = obs.loc[obs.oname.apply(lambda x: x in onames)]
#     # only non-zero observations
# #     obs = obs.loc[obs.obgnme.apply(lambda x: x in pst.nnz_obs_groups),:]
#     # make a plot
#     ogs = obs.obgnme.unique()
#     fig,axes = plt.subplots(len(ogs),1,figsize=(width,height*len(ogs)))
#     ogs.sort()
#     # for each observation group (i.e. timeseries)
#     for ax,og in zip(axes,ogs):
#         # get values for x axis
#         oobs = obs.loc[obs.obgnme==og,:].copy()
#         oobs.loc[:,"time"] = oobs.loc[:,"time"].astype(str)
# #         oobs.sort_values(by="time",inplace=True)
#         tvals = oobs.time.values
#         onames = oobs.obsnme.values
#         if dot is True:
#             # plot prior
#             [ax.scatter(tvals,pr_oe.loc[i,onames].values,color="gray",s=30, alpha=0.5) for i in pr_oe.index]
#             # plot posterior
#             [ax.scatter(tvals,pt_oe.loc[i,onames].values,color='b',s=30,alpha=0.2) for i in pt_oe.index]
#             # plot measured+noise 
#             oobs = oobs.loc[oobs.weight>0,:]
#             tvals = oobs.time.values
#             onames = oobs.obsnme.values
#             ax.scatter(oobs.time,oobs.obsval,color='red',s=30).set_facecolor("none")
#         if dot is False:
#             # plot prior
#             [ax.plot(tvals,pr_oe.loc[i,onames].values,"0.5",lw=0.5,alpha=0.5) for i in pr_oe.index]
#             # plot posterior
#             [ax.plot(tvals,pt_oe.loc[i,onames].values,"b",lw=0.5,alpha=0.5) for i in pt_oe.index]
#             # plot measured+noise 
#             oobs = oobs.loc[oobs.weight>0,:]
#             tvals = oobs.time.values
#             onames = oobs.obsnme.values
#             ax.plot(oobs.time,oobs.obsval,"r-",lw=2)
#         ax.tick_params(axis='x', labelrotation=90)
#         ax.margins(x=0.01)
#         ax.set_title(og,loc="left")
#     # fig.tight_layout()
#     plt.show()




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
    # so_df = pd.concat([simm.ch4prod, obd.ch4_obd], axis=1).dropna(axis=0)
    os.chdir(wd)
    # plot_one_one(so_df)
    plot_oom(so_df)