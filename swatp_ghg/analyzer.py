import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from swatp_ghg.utils import ObjFns
import numpy as np
import pandas as pd
import os
from swatp_ghg.models import DCmodel


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


def plot_oom(df, target=None, numcols=1, fsize=8):
    m1 = ObjFns()
    if target is None:
        target = "ch4e_tot"

    fig, ax = plt.subplots(figsize=(6,5))
    colors = cm.rainbow(np.linspace(0, 1, len(df.cont.unique())))
    print(df)
    fmax = df.loc[:, [target, "ch4_obd"]].max().max()
    fmin = df.loc[:, [target, "ch4_obd"]].min().min()
    x_val = df.loc[:, target].tolist()
    y_val = df.loc[:, "ch4_obd"].tolist()
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