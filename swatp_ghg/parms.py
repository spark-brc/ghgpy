
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
        self.frCH4emit_p = 0.55 # MaXimum Fraction of CH4 production emitted by plants. (MXCH4F)
        self.frac_to_exd = 0.45 # range(0 - 1)
        self.tmxbio = 1260 # (rice)
        self.q10 = 3.0
        self.frCH4emit_b = 0.7 # the fraction of CH4 emitted via bubbles






