
class DCparms(object):
    
    def __init__(self):
        self.aeh = 0.23 # range: 
        self.deh = 0.16 # range:
        self.beh_flood = -250 # Lower limit value for Eh during flooding course (mv)
        self.beh_drain = 300
        self.zero_root_frac = 0.7 # (0-1)
        self.ch4rootlim = 1.0 
        self.co2_to_ch4 = 0.5
        self.frCH4emit = 0.55
        self.frac_to_exd = 0.45 # range(0 - 1)
        self.tmxbio = 1260 # (rice)
        self.q10 = 3.0






