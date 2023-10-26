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
import os
import math
import numpy as np
from ghgpy.parms import DCparms, MERESparms, DNDCparms
import pandas as pd


class DCmodel(object):
    def __init__(self, model_dir):
        self.model_dir = model_dir
        # self.beta1, self.Rh, self.fracToExduates, self.sand_cont = self.read_parms()
        self.parms = DCparms()


    def ch4prod(self, sand_cont, eh_t, t_soil, root_c_prod):
        """CH4 production was simulated based on carbon substrate supply and 
        associated influence of Eh and temperature

        Args:
            eh_t (float, mV): initial redox potential
            sand_cont (float):  the average sand content fraction (sand, 0.0 - 1.0) in the top 10 cm of soil
            t_soil (float, ◦C): average soil temperature in the top 10 cm of soil (◦C)
            root_c_prod (float, gC m^-2 d^-1): the previous day's fine root production estimated by 
            the plant production submodel in DayCent (gC m^-2 d^-1)

        Returns:
            float, g CH4-C m^-2d^-1: CH4Prod is the CH4 production rate (g CH4-C m^-2d^-1)
        """
        ch4prod_ = (
            self.parms.cvfr_cho_to_ch4 * 
            self.feh(eh_t) * 
            (self.c_soil(sand_cont) + self.f_temp(t_soil) * self.c_root(sand_cont, root_c_prod))
            )
        return ch4prod_



    # def read_parms(self):
    #     beta1 = 1
    #     Rh = 1
    #     fracToExduates = 0.5
    #     sand_cont= 0.5

    #     return beta1, Rh, fracToExduates, sand_cont
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

    def c_soil(self, sand_cont):
        """The first step in modeling methanogenesis is to estimate 
        the amount of carbon substrate available for CH4 production. 
        DayCent's methanogenesis submodel includes soil organic matter degradation and 
        rhizodeposition as the sources of carbon.

        :arg sand_cont2: test
        :type sand_cont2: float
        :param sand_cont: _description_
        :type sand_cont: _type_
        :return: _description_
        :rtype: _type_
        """


        c_soil_ = self.parms.cvcf_oc_to_co2 * self.parms.frToCH4 * self.soil_index(sand_cont) * self.parms.hr
        return c_soil_


    def soil_index(self, sand_cont):
        """calculate soil texture index

        Args:
            sand_cont (float): index which is a function of the average sand content fraction 
            (sand, 0.0 - 1.0) in the top 10 cm of soil

        Returns:
            float: soil texture index
        """
        soil_index_ = 0.325+2.25* sand_cont
        return soil_index_
    

    def c_root(self, root_c_prod, sand_cont):
        """The rate of rhizodeposition (Croot, gC m^-2 d^-1) is calculated using 
        the following equation.

        Args:
            frac_to_exudates (float): the fraction of root carbon production contributing to 
            rhizodeposition (range of 0.35-0.6 described in Cao et al. (1995))
            root_c_prod (_type_): the previous day's fine root production estimated by 
            the plant production submodel in DayCent (gC m^-2 d^-1)
        """
        si = self.soil_index(sand_cont)


        c_root_ = self.parms.frac_to_exd * si * root_c_prod
        return c_root_
    
    def f_temp(self, t_soil):
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
        q10 = self.parms.q10

        if t_soil > 30:
            t_soil = 30
            f_t = q10 **((t_soil-30)/10)
        else:
            f_t = q10 **((t_soil-30)/10)
        return f_t


    def feh(self, eh_t):
        """FEh, a reduction factor for soil redox potential (Eh) (mV), is 
        estimated using the following equations from Huang et al. (1998) and 
        Huang et al. (2004):

        Args:
            eh_t (float, mV): Eht represents the Eh value at time t, and 
            t is the number of days after flooding began or 
            since drainage occurred in the cycle.
        """
        if eh_t >= -150:
            feh_t = math.exp(-1.7*(150+eh_t)/150)
        else:
            eh_t = -150
            feh_t = math.exp(-1.7*(150+eh_t)/150)
        return feh_t


    def get_eh(
            self, sand_cont, waterlevel, eh_init):
        """DEh and AEh (DEH and AEH, fix.100) are differential coefficients that 
        were estimated as 0.16 and 0.23, respectively. 
        The BEhflood (BEHFL, fix.100) is set at a low-limit value of -250 mV, 
        and Behdrain (BEHDR, fix.100) is set to an upper-limit value of 300 mV (Cao et al. 1995, Huang et al. 2004). 
        Soil Eh is a constant value of -20 mV when intermittent irrigation is used in 
        rice paddies as discussed in Huang et al. (2004).

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
            waterlevel (_type_): _description_
            eh_t (_type_): _description_
            deh (float, optional): _description_. Defaults to 0.16.
            aeh (float, optional): _description_. Defaults to 0.23.
            beh_flood (int, optional): _description_. Defaults to -250.
            beh_drain (int, optional): _description_. Defaults to 300.

        Returns:
            float, mV: current eh
        """


        c_soil = self.c_soil(sand_cont)

        if waterlevel == "flooding":
            eh_now = eh_init - (self.parms.deh * (self.parms.aeh + min(1, c_soil)) * (eh_init - self.parms.beh_flood))
        elif waterlevel == "draining":
            eh_now = eh_init - (self.parms.deh * (self.parms.aeh + 0.7) * (eh_init - self.parms.beh_drain))
        else: # water added via rain and irrigation events
            eh_now = -20
        return eh_now        


    def ch4ep(self, fp, ch4prod):
        """CH4 emission rates through the rice plants (CH4EP) (g CH4-C m^-2d^-1) were simulated

        Args:
            fp (float): fraction of CH4 emitted via rice plants
            ch4prod (float): CH4Prod is total methane production (g CH4-C m^-2d^-1)
        Returns:
            float: transport of CH4 via ebullition to the atmosphere (CH4Ebl)
        """

        ch4ep_ = fp * ch4prod
        return ch4ep_


    def fp(self, aglivc):
        """ get the fraction of CH4 emitted via rice plants

        Args:
            aglivc (float, g C m^-2): the amount of above-ground live C for the crop as simulated by DayCent (g C m^-2)
            tmxbio (float, g biomass m^-2): the maximum aboveground biomass at the end of growing season
            mxch4f (float, optional): MaXimum Fraction of CH4 production emitted by plants. Defaults to 0.55.

        Returns:
            float: the fraction of CH4 emitted via rice plants
        """
        # the multiplier 2.5 (g biomass/g C) converts C to biomass (g biomass m^-2)
        fp_ = self.parms.mxch4f * (1.0 - (aglivc * 2.5/self.parms.tmxbio))**0.25

        return fp_
    
    def ch4ebl(self, tsoil, ch4prod, ch4ep, bglivc):
        """transport of CH4 via ebullition to the atmosphere (CH4Ebl) was also adopted from Huang et al. (2004)

        Args:
            methzr (float): fraction of CH4 emitted via bubbles when there is zero fine root biomass
            tsoil (_type_): 
            ch4prod (_type_): _description_
            ch4ep (_type_): _description_
            mo (float, gC m^-2d^-1): Mo was set to 0.0015 gC m^-2d^-1 (Huang et al. 2004) but is set to 0.002 in DayCent
            mrtblm (float, g biomass m-2): the root biomass that starts to reduce CH4 bubble formation (g biomass m-2)
            bglivc (float, g C m^-2): the amount of fine root C for the crop as simulated by DayCent (g C m^-2)

        Returns:
            float: transport of CH4 via ebullition to the atmosphere (CH4Ebl)
        """
        
        # the multiplier 2.5 (g biomass/g C) converts C to biomass
        # CH4 ebullition is reduced when Tsoil < 2.718282 °C.
        ch4ebl_ = (
            self.parms.frCH4emit_b * 
            (ch4prod - ch4ep - self.parms.mo) * 
            min(np.log(tsoil), 1.0) * 
            (self.parms.mrtblm/(bglivc*2.5))
            )
        return ch4ebl_
    
    def read_inputs(self):
        input_df = pd.read_csv(
            os.path.join(
                self.model_dir, "input_ghg.csv"), na_values=[-9999, ""],
                index_col=0, parse_dates=True)
        return input_df
    

class MERES(object):
    def __init__(self, model_dir):
        self.model_dir =  model_dir
        self.parms = MERESparms()

    def ch4prod(self, pch4prod, o2conc):
        """Actual CH4 production (PCH4, mol m-3 s-1) in a given soil layer

        Args:
            pch4prod (float, mol C m-3 s-1): potential CH4 production
            o2conc (float, mol m-3): concentration of O2

        Returns:
            float: Actual CH4 production (PCH4, mol m-3 s-1)
        """
        ch4prod_ = pch4prod / (1 + (self.parms.eta *o2conc))
        return ch4prod_



    def c_root(self, root_wt):
        """the rate of root exudation (g\ C\ m^{-2}d^{-1}) is calculated as 
        the product of organic compounds per unit of root biomass 
        (depending on the crop growth stage) and 
        the root weight in each soil layer based on results from Lu et al. (1999).

        Args:
            root_wt (float, kg\ DM\ {ha}^{-1})): existing root dry weight in each soil layer per day

        Returns:
            float: the rate of root exudation
        """
        return 0.4*0.02* root_wt
    
    def pch4prod(self, aex, subst_c_prod):
        """potential CH4 production (PCH4*, mol C m-3 s-1)

        Args:
            aex (float, mol Ceq m-3): alternative electron acceptors in oxidized form ({AEX}_{ox})
            subst_c_prod (_type_): the rate of substrate-C production (mol Ceq m-3 s-1)

        Returns:
            float, mol C m-3 s-1: potential CH4 production 
        """
        if aex > self.parms.c_aex:
            pch4prod_ = 0.0
        elif aex > 0.0 and aex < self.parms.c_aex:
            pch4prod_ = min(0.2 * (1-(aex/self.parms.c_aex)), subst_c_prod)
        elif aex == 0:
            pch4prod_ = subst_c_prod
        return pch4prod_

    def ch4oxid(self, pch4prod, ch4conc, o2conc):
        """The rate of CH4 consumption (QCH4, mol m-3 s-1) by 
            the methanotrophic bacteria (see equation 2) in 
            a soil layer is given by the Michaelis-Menten equation
        .. math:: 
            p=f(x)


        :param pch4prod: potential CH4 production
        :type pch4prod: float, mol Ceq m-3
        :param ch4conc: ch4 concentration
        :type ch4conc: float, mol m-3
        :param o2conc: o2 concentration
        :type o2conc: float, mol m-3
        :return: rate of CH4 consumption
        :rtype: float, mol m-3 s-1
        """
        ch4oxid_ = (
            pch4prod * 
            (ch4conc/(self.parms.k1 + ch4conc)) * 
            (o2conc/(self.parms.k2 + o2conc))
        )
        # self.parms.
        return ch4oxid_
    
    def o2cons(self, o2conc, ch4oxid, pch4prod):
        """Oxygen consumption rate (QO2, mol m-3 s-1)

        :param o2conc: o2 concentration
        :type o2conc: float, mol m-3
        :param ch4oxid: rate of CH4 consumption
        :type ch4oxid: float, mol m-3 s-1
        :param pch4prod: potential CH4 production
        :type pch4prod: float, mol C m-3 s-1
        :return: Oxygen consumption rate
        :rtype: float, mol C m-3 s-1
        """
        o2cons_ = 2*ch4oxid + 2*pch4prod * (o2conc / (self.parms.k3 + o2conc))
        return o2cons_

    # NOTE: Should we distinguish between O2 concentration and its concentration in the gaseous phase?
    def o2flux(self, o2conc):
        """the fluxes of O2

        :param o2conc: o2 concentration
        :type o2conc: float, mol m-3
        :return: the fluxes of O2
        :rtype: float, mol m-3 s-1
        """
        
        o2flux_ = (
            self.parms.sc_root * 
            (self.parms.root_len_den * 10e+04) * 
            self.parms.o2dfc *
            (self.parms.o2conc_atm - o2conc)
        )
        return o2flux_


    def ch4ebl(self, ch4conc_sol):
        """We have modified the algorithm describing ebullition rate from that in the original Arah & Kirk (2000) model by 
        expressing the rate of ebullition (E, mol m-3 s-1) as a function of the concentration of 
        the substance in solution (yw, mol m-3). 
        Currently, there is no temperature dependence of yw* included in the model. 


        :param ch4conc_sol: concentration of the substance in solution
        :type ch4conc_sol: float, mol m-3
        :return: rate of ebullition
        :rtype: float, mol m-3 s-1
        """

        ch4ebl_ = max(
            0, 
            (ch4conc_sol - self.parms.ch4sol)/self.parms.ke
            )
        return ch4ebl_
    

    def o2ebl(self, o2conc_sol):
        """We have modified the algorithm describing ebullition rate from that in the original Arah & Kirk (2000) model by 
        expressing the rate of ebullition (E, mol m-3 s-1) as a function of the concentration of 
        the substance in solution (yw, mol m-3). 
        Currently, there is no temperature dependence of yw* included in the model. 


        :param ch4conc_sol: concentration of the substance in solution
        :type ch4conc_sol: float, mol m-3
        :return: rate of ebullition
        :rtype: float, mol m-3 s-1
        """

        o2ebl_ = max(
            0, 
            (o2conc_sol - self.parms.o2sol)/self.parms.ke
            )
        return o2ebl_
    


class DNDC(object):
    def __init__(self, model_dir):
        self.model_dir =  model_dir
        self.parms = DNDCparms()

    def ch4prod(self, ava_c, ft_temp):

        ch4prod_ = self.parms.a * ava_c * ft_temp
        return ch4prod_
    
    def ft_temp(self, temp):
        ft_temp_ = self.parms.b * math.exp(0.2424*temp)
        return ft_temp_

    def ch4oxid(self, ch4conc, eh):
        ch4oxid_ = ch4conc * math.exp(8.6711*eh/1000)
        return ch4oxid_
    
    def ch4ep(self, ch4prod, aere):
        ch4ep_ = 0.5 * ch4prod * aere
        return ch4ep_
    
    def aere(self, pgi):
        """ Calculate AERE (Aerobic Respiration Enhancement) based on the Polynomial Equation.

        :param pgi: Plant Growth Index.
        :type pgi: float
        :return: The calculated AERE value.
        :rtype: float
        """
        # Define coefficients for the polynomial equation
        a = -0.0009
        b = 0.0047
        c = -0.883
        d = 1.9863
        e = -0.3795
        f = 0.0251

        # Calculate AERE using the polynomial equation
        aere_ = a * pgi**5 + b * pgi**4 + c * pgi**3 + d * pgi**2 + e * pgi + f
        return aere_
    
    def pgi(self, dsp, sds):
        pgi_ = dsp / sds
        return pgi_
    
    def ch4ebl(self, ch4prod, poro, ft_temp2, aere):
        """Calculate CH4 emission via ebullition based on various factors.

        :param ch4prod: Total methane production.
        :type ch4prod: float
        :param poro: Soil porosity.
        :type poro: float
        :param ft_temp2: Temperature-based factor.
        :type ft_temp2: float
        :param aere: aerenchyma factor
        :type aere: float
        :return: CH4 emission via ebullition.
        :rtype: float
        """

        ch4ebl_ = 0.25 * ch4prod* poro * ft_temp2 * (1 - aere)
        return ch4ebl_

    def ft_temp2(self, t_soil):
        """Calculate a temperature-based factor (ft_temp2) based on a polynomial equation.

        :param t_soil: The average soil temperature in °C.
        :type t_soil: float
        :return: The calculated temperature-based factor (ft_temp2).
        :rtype: float
        """

        # Coefficients for the polynomial equation
        a = -0.1687
        b = 1.167
        c = -2.0303
        d = 1.042

        # Calculate ft_temp2 using the polynomial equation
        t_soil_normalized = 0.1 * t_soil
        ft_temp2_ = a * t_soil_normalized**3 + b * t_soil_normalized**2 + c * t_soil_normalized + d

        return ft_temp2_