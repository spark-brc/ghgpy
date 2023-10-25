
class DCparms(object):
    
    def __init__(self):
        self.cvfr_cho_to_ch4 = 0.5 # conversion factor of carbohydrate decomposition to CO2 and CH4 (dimensionless) 
                                    # C6H12O6_to_CH4 (alpha1)
        self.cvcf_oc_to_co2 = 0.5 # conversion coefficient on a mole weight basis of organic carbon to CO2 
                                    #calculated as 0.5 (alpha2)
        self.frToCH4 = 0.15 # the fraction of heterotrophic respiration converted to CH4 under anaerobic conditions
                            # beta1
        self.frToExudate = 0.45 # fraction of root carbon production contributing to rhizodeposition (fracToExudates)
                            # range 0.35-0.6 beta2 FREXUD 0.0 - 1.0
        self.hr = 0.1 # Rh is heterotrophic respiration from decomposition of organic matter 
                        #(above- and below-ground structural and metabolic litter and above- and below-ground SOC pools) 
                        # (g CO2-C m−2 d−1)
                        # NOTE: is this daily simulated input or parameter?
        self.aeh = 0.23 # range: 
        self.deh = 0.16 # range:
        self.beh_flood = -250 # Lower limit value for Eh during flooding course (mv)
        self.beh_drain = 300
        self.eh_rain_irr = -20
        self.zero_root_frac = 0.7 # (0-1)
        self.ch4rootlim = 1.0 
        self.co2_to_ch4 = 0.5
        self.mxch4f = 0.55 # MaXimum Fraction of CH4 production emitted by plants. (MXCH4F)
        self.frac_to_exd = 0.45 # range(0 - 1)
        self.tmxbio = 1260 # (rice)
        self.q10 = 3.0
        self.frCH4emit_b = 0.7 # the fraction of CH4 emitted via bubbles
        self.mo = 0.002 # Mo was set to 0.0015 gC m−2d−1 (Huang et al. 2004) but is set to 0.002 in DayCent
        self.mrtblm = 1.0 # Root biomass that when exceeded starts to reduce methane bubble formation (g biomass m-2)


# class DNDCparms_org(object):
#     """_summary_

#     :param object: _description_
#     :type object: _type_
#     """
#     def __init__(self):
#         self.c_aex = 24.0 # the critical concentration of the oxidized alternative electron acceptor pool (mol Ceq m-3)
#         self.eta = 400 # parameter (units: m3 mol-1) representing the sensitivity of methanogenesis to 
#                         # the concentration of O2 ([O2], mol m-3), 
#                         # A value of 400 m3 mol-1 was used for η (Arah & Stephen, 1998).
#         self.k1 = 0.33 # k1 and k2 are Michaelis-Menten constants (units: mol m-3) for 
#                         # a dual-substrate reaction.
#         self.k2 = 0.44 # k1 and k2 are Michaelis-Menten constants (units: mol m-3) for 
#                         # a dual-substrate reaction.
#         self.k3 = 0.22 # k1 and k2 are Michaelis-Menten constants (units: mol m-3) for 
#                         # a dual-substrate reaction.
#         self.sc_root = 0.1 # the specific conductivity (units: m air (m root)-1) of the root system.
#         self.o2conc_atp = 7.76



class DNDCparms(object):
    """_summary_

    :param object: _description_
    :type object: _type_
    """
    def __init__(
            self,
            c_aex=24.0,
            eta=400,
            k1=0.33,
            k2=0.44,
            k3=0.22,
            sc_root=0.1,
            o2conc_atp=7.76):
        """_summary_

        :param c_aex: _description_, defaults to 24.0
        :type c_aex: float, optional
        :param eta: _description_, defaults to 400
        :type eta: int, optional
        :param k1: _description_, defaults to 0.33
        :type k1: float, optional
        """

        self.c_aex = c_aex # the critical concentration of the oxidized alternative electron acceptor pool (mol Ceq m-3)
        self.eta = eta # parameter (units: m3 mol-1) representing the sensitivity of methanogenesis to 
                        # the concentration of O2 ([O2], mol m-3), 
                        # A value of 400 m3 mol-1 was used for η (Arah & Stephen, 1998).
        self.k1 = k1 # k1 and k2 are Michaelis-Menten constants (units: mol m-3) for 
                        # a dual-substrate reaction.
        self.k2 = k2# k1 and k2 are Michaelis-Menten constants (units: mol m-3) for 
                        # a dual-substrate reaction.
        self.k3 = k3 # k1 and k2 are Michaelis-Menten constants (units: mol m-3) for 
                        # a dual-substrate reaction.
        self.sc_root = sc_root # the specific conductivity (units: m air (m root)-1) of the root system.
        self.o2conc_atp = o2conc_atp

