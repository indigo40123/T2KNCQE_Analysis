class NCQE_Cut:
    def __init__(self, run, anamode):
        self.run = str(run)
        self.anamode = int(anamode)
        self.lowecut = self._set_loweBGcut(run)
        self.aopt, self.bopt = self._set_ChereAngleCut(anamode)
     
    def _set_loweBGcut(self, run):
        cuts = {
          # dwall
          ( "dwall",   "1"  ) : ( -70.0,   559.2 ),
          ( "dwall",   "2"  ) : ( -60.0,   508.3 ),
          ( "dwall",   "3b" ) : ( -40.0,   410.0 ),
          ( "dwall",   "3c" ) : ( -40.0,   406.7 ),
          ( "dwall",   "4"  ) : ( -80.0,   580.0 ),
          ( "dwall",   "5a" ) : ( -80.0,   580.0 ),
          ( "dwall",   "5b" ) : ( -80.0,   580.0 ),
          ( "dwall",   "5c" ) : ( -80.0,   580.0 ),
          ( "dwall",   "6a" ) : ( -80.0,   580.0 ),
          ( "dwall",   "6b" ) : (-100.0,   675.0 ),
          ( "dwall",   "6c" ) : (-100.0,   675.0 ),
          ( "dwall",   "6d" ) : (-100.0,   675.0 ),
          ( "dwall",   "6e" ) : (-100.0,   675.0 ),
          ( "dwall",   "6f" ) : ( -80.0,   580.0 ),
          ( "dwall",   "7a" ) : ( -80.0,   580.0 ),
          ( "dwall",   "7b" ) : ( -80.0,   580.0 ),
          ( "dwall",   "7c" ) : ( -80.0,   580.0 ),
          ( "dwall",   "8"  ) : ( -80.0,   580.0 ),
          ( "dwall",   "9a" ) : ( -80.0,   580.0 ),
          ( "dwall",   "9b" ) : ( -80.0,   580.0 ),
          ( "dwall",   "9c" ) : ( -80.0,   580.0 ),
          ( "dwall",   "9d" ) : ( -80.0,   580.0 ), 
          ( "dwall",   "10a") : ( -80.0,   580.0 ), #take Run9 temporary
          ( "dwall",   "10b") : ( -80.0,   580.0 ), #take Run9 temporary
          ( "dwall",   "11" ) : ( -80.0,   580.0 ),
          # effwall
          ( "effwall", "1"  ) : ( -332.0,  2257.0 ),
          ( "effwall", "2"  ) : ( -300.0,  2087.0 ),
          ( "effwall", "3b" ) : ( -352.0,  2334.0 ),
          ( "effwall", "3c" ) : ( -352.0,  2334.0 ),
          ( "effwall", "4"  ) : ( -332.0,  2205.0 ),
          ( "effwall", "5a" ) : ( -350.0,  2309.5 ),
          ( "effwall", "5b" ) : ( -350.0,  2309.5 ),
          ( "effwall", "5c" ) : ( -296.0,  2090.0 ),
          ( "effwall", "6a" ) : ( -344.0,  2276.0 ),
          ( "effwall", "6b" ) : ( -452.0,  2810.0 ),
          ( "effwall", "6c" ) : ( -452.0,  2810.0 ),
          ( "effwall", "6d" ) : ( -452.0,  2810.0 ),
          ( "effwall", "6e" ) : ( -452.0,  2810.0 ),
          ( "effwall", "6f" ) : ( -352.0,  2314.0 ),
          ( "effwall", "7a" ) : ( -322.0,  2136.5 ),
          ( "effwall", "7b" ) : ( -290.0,  1988.5 ),
          ( "effwall", "7c" ) : ( -322.0,  2136.5 ),
          ( "effwall", "8"  ) : ( -266.0,  1804.5 ),
          ( "effwall", "9a" ) : ( -288.0,  1940.0 ),
          ( "effwall", "9b" ) : ( -294.0,  1987.5 ),
          ( "effwall", "9c" ) : ( -294.0,  1987.5 ),
          ( "effwall", "9d" ) : ( -294.0,  1987.5 ),
          ( "effwall", "10a") : ( -294.0,  1987.5 ), #take Run9 temporary
          ( "effwall", "10b") : ( -294.0,  1987.5 ), #take Run9 temporary
          ( "effwall", "11" ) : ( -314.0,  1941.5 ),
          # ovaQ
          ( "ovaQ",    "1"  ) : ( -0.0420,  0.4045 ),
          ( "ovaQ",    "2"  ) : ( -0.0480,  0.4340 ),
          ( "ovaQ",    "3b" ) : ( -0.0380,  0.3835 ),
          ( "ovaQ",    "3c" ) : ( -0.0420,  0.4025 ),
          ( "ovaQ",    "4"  ) : ( -0.0360,  0.3690 ),
          ( "ovaQ",    "5a" ) : ( -0.0440,  0.4090 ),
          ( "ovaQ",    "5b" ) : ( -0.0440,  0.4090 ),
          ( "ovaQ",    "5c" ) : ( -0.0440,  0.4130 ),
          ( "ovaQ",    "6a" ) : ( -0.0320,  0.3440 ),
          ( "ovaQ",    "6b" ) : ( -0.0360,  0.3910 ),
          ( "ovaQ",    "6c" ) : ( -0.0360,  0.3910 ),
          ( "ovaQ",    "6d" ) : ( -0.0360,  0.3950 ),
          ( "ovaQ",    "6e" ) : ( -0.0360,  0.3910 ),
          ( "ovaQ",    "6f" ) : ( -0.0320,  0.3440 ),
          ( "ovaQ",    "7a" ) : ( -0.0380,  0.3595 ),
          ( "ovaQ",    "7b" ) : ( -0.0320,  0.3620 ),
          ( "ovaQ",    "7c" ) : ( -0.0380,  0.3595 ),
          ( "ovaQ",    "8"  ) : ( -0.0420,  0.3985 ),
          ( "ovaQ",    "9a" ) : ( -0.0480,  0.4140 ),
          ( "ovaQ",    "9b" ) : ( -0.0420,  0.4125 ),
          ( "ovaQ",    "9c" ) : ( -0.0420,  0.4125 ),
          ( "ovaQ",    "9d" ) : ( -0.0420,  0.4125 ),
          ( "ovaQ",    "10a") : ( -0.0420,  0.4125 ), #take Run9 temporary
          ( "ovaQ",    "10b") : ( -0.0420,  0.4125 ), #take Run9 temporary
          ( "ovaQ",    "11" ) : ( -0.0420,  0.4125 )
        }
        return cuts

    def _set_ChereAngleCut(self, anamode):
        if self.anamode == 4 :
            aopt = 1.67832
            bopt = 17.7273
        elif self.anamode == 5 :
            aopt = 1.78322
            bopt = 15.0
        elif anamode == 6 :
            aopt = 1.67832
            bopt = 15.0
        elif anamode == 7 : # take Run11 setting temporary for Run 10
            aopt = 1.67832
            bopt = 15.0
        else :
            raise ValueError(f"Unknown anamode: {self.run_number}")
        return aopt, bopt

    def cut_val(self, var, run, energy ) :
        m, b = self.lowecut[(var, str(run))]
        return m * energy + b

    def is_NCQE(self, Erec, dwall, effwall, ovaq, angle):
        ## 0. Good spill cut (only for Data)

        ## 1. Energy cut (Selection: 4 <= Erec < 30 MeV)
        if Erec >= 30 : return False
        if Erec < 4   : return False

        ## 2. Timing cut (only for Data, Selection: bunch center +/-100 ns)

        ## 3. Fiducial volume cut
        if dwall < 200   : return False
        if effwall < 200 : return False

        ## 4. Fit quality cut  * dwall/effwall/ovaQ are optimized
        if dwall    < self.cut_val("dwall",    self.run, Erec ) : return False
        if effwall  < self.cut_val("effwall", self.run, Erec ) : return False
        if ovaq     < self.cut_val("ovaQ",    self.run, Erec ) : return False

        ## 5. Pre-activity cut to remove muon-decay-e
        #if tree.n30 > 22 : return False

        ## 6. Cherenkov angle cut (Selection: thetaC >= 34 deg)
        if angle < self.aopt * Erec + self.bopt : return False

        return True


    def channel(self, Neutmode):
        if (Neutmode == 51 or Neutmode == 52) : return "nuncqe"
        if (Neutmode == -51 or Neutmode == -52) : return "nubarncqe"
        if (abs(Neutmode) > 30 and abs(Neutmode) < 35) : return "nc1pi"
        if (abs(Neutmode) > 30) : return "ncother"
        if (abs(Neutmode) == 1) : return "ccqe"
        if (abs(Neutmode) == 2) : return "ccqe2p2h"
        if (Neutmode == 0) : return "ccother"
        else : return "others"







