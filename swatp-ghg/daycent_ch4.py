"""
Hartman, M.D., Parton, W.J., Grosso, S.J.D., Easter, M., Hendryx, J., Hilinski, T., Kelly, R., 
Keough, C.A., Killian, K., Lutz, S., Marx, E., McKeown, R., Ogle, S., Ojima, D.S., Paustian, K., 
Swan, A., Williams, S., n.d. 
The Daily Century Ecosystem, Soil Organic Matter, Nutrient Cycling, Nitrogen Trace Gas, 
and Methane Model User Manual, Scientific Basis, and Technical Documentation.

Anaerobic carbohydrate fermentation and methanogenesis occur through the following reactions, 
2(CH2O) → CO2+ CH4 (Conrad 1989, Matthews et al. 2000) or C6H12O6→ 3CO2+ 3CH4 (Huang et al. 1998). 
Both of these equations illustrate that the carbon substrate producing CH4 also produces 
the same carbon equivalent of CO2. 
Hence, a conversion factor C6H12O6_to_CH4 on a mole weight basis of carbohydrate to CH4 is set 
at 0.5 based on the reactions.

"""

import math


class ghg(object):
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.fac_c_subt_to_ch4 = 0.5

    def c_soil(self, beta1, SI, Rh):
        """The first step in modeling methanogenesis is to estimate 
        the amount of carbon substrate available for CH4 production. 
        DayCent's methanogenesis submodel includes soil organic matter degradation and 
        rhizodeposition as the sources of carbon.

        Args:
            beta1 (float): A fraction (β1) is defined to quantify 
                        the amount of substrate available for methanogens based on 
                        the simulation of heterotrophic respiration by the DayCent model.
                        β1 (CO2CH4, fix.100) is the fraction of Rh converted to CH4 under 
                        anaerobic conditions;
            SI (_type_): _description_
            Rh (float): Rh is heterotrophic respiration from decomposition of organic matter
                        (above- and below-ground structural and metabolic litter and 
                        above- and below-ground SOC pools) (g CO2^-C m^-2 d^-1)
        """


        self.c_soil_ = self.fac_c_subt_to_ch4 * beta1 * SI * Rh
        return self.c_soil_


    def SI(self, send_cont_frac=0.5):
        """calculate soil texture index

        Args:
            send_cont_frac (float): index which is a function of the average sand content fraction 
            (sand, 0.0 - 1.0) in the top 10 cm of soil

        Returns:
            float: soil texture index
        """
        self.si_ = 0.325+2.25*send_cont_frac
        return self.si_
    

    def c_root(self, frac_to_exudates, root_c_prod):
        """The rate of rhizodeposition (Croot, gC m^-2 d^-1) is calculated using 
        the following equation.

        Args:
            frac_to_exudates (float): the fraction of root carbon production contributing to 
            rhizodeposition (range of 0.35-0.6 described in Cao et al. (1995))
            root_c_prod (_type_): the previous day's fine root production estimated by 
            the plant production submodel in DayCent (gC m^-2 d^-1)
        """
        self.c_root_ = frac_to_exudates * self.si_ * root_c_prod
        return self.c_root_
    
    def f_temp(self, t_soil, q10=3.0):
        """estimate the influence of soil temperature. To simulate CH4 production, 
        we adopted the approach by (Huang et al. 1998) and (Huang et al. 2004).

        Args:
            t_soil (float): the average soil temperature in the top 10 cm of soil (◦C)
            q10 (float, optional): a temperature coefficient representing the change of a biological or 
            chemical system as a consequence of increasing the temperature by 10°C, 
            and was assumed to be a value of 3.0 (Huang et al. 1998). Defaults to 3.0.

        Returns:
            _type_: _description_
        """


        if t_soil >= 30:
            self.f_t = q10 **((t_soil-30)/10)
        return self.f_t


    def feh(self, eh_t):
        """FEh, a reduction factor for soil redox potential (Eh) (mV), is 
        estimated using the following equations from Huang et al. (1998) and 
        Huang et al. (2004):

        Args:
            eh_t (float, mV): Eht represents the Eh value at time t, and 
            t is the number of days after flooding began or 
            since drainage occurred in the cycle.
        """
        if eh_t <= -150:
            feh_t = math.exp(-1.7*(150+eh_t)/150)

    def get_eh(
            self, beta1, SI, Rh, waterlevel, eh_t,
            deh=0.16, aeh=0.23, beh_flood=-250, beh_drain=300):
        """DEh and AEh (DEH and AEH, fix.100) are differential coefficients that 
        were estimated as 0.16 and 0.23, respectively. 
        The BEhflood (BEHFL, fix.100) is set at a low-limit value of -250 mV, 
        and Behdrain (BEHDR, fix.100) is set to an upper-limit value of 300 mV (Cao et al. 1995, Huang et al. 2004). 
        Soil Eh is a constant value of -20 mV when intermittent irrigation is used in 
        rice paddies as discussed in Huang et al. (2004).

        Args:
            beta1 (_type_): _description_
            SI (_type_): _description_
            Rh (_type_): _description_
            waterlevel (_type_): _description_
            eh_t (_type_): _description_
            deh (float, optional): _description_. Defaults to 0.16.
            aeh (float, optional): _description_. Defaults to 0.23.
            beh_flood (int, optional): _description_. Defaults to -250.
            beh_drain (int, optional): _description_. Defaults to 300.

        Returns:
            _type_: _description_
        """


        




        c_soil = self.c_soil(beta1, SI, Rh)




        if waterlevel == "flooding":
            eh_now = eh_t - (deh * (aeh + min(1, c_soil)) * (eh_t - beh_flood))
        elif waterlevel == "draining":
            eh_now = eh_t - (deh * (aeh + 0.7) * (eh_t - beh_drain))
        else: # water added via rain and irrigation events
            eh_now = -20
        return eh_now        


