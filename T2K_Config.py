from collections import defaultdict
from ROOT import TFile
import os

class T2K:
    def __init__(self, anamode):
        self.L, self.osca, self.oscb, self.deltam32 = self._set_osc_para()
        self.nudir = self._set_nudir()

        self.anamode = int(anamode)
        self.ncel_scales = self._set_ncel_scales()
        self.runs, self.fluxtunes = self._set_fluxtune()
        self.pot = { #---- FHC ----
                     "1": 0.32675e20,
                     "2": 1.12206e20,
                    "3b": 0.21777e20,
                    "3c": 1.38228e20,
                     "4": 3.59728e20,
                    "5a": 0.06669e20,
                    "5b": 0.17877e20,
                    "6a": 0.10309e20,
                    "6f": 0.08984e20,
                    "7a": 0.08967e20,
                    "7c": 0.39629e20,
                     "8": 7.17065e20,
                    "9a": 0.20432e20,
                   "10a": 2.62400e20,
                   "10b": 2.10200e20,
                    "11": 1.76000e20,
                    #---- RHC ----
                    "5c": 0.51450e20,
                    "6b": 1.31353e20,
                    "6c": 0.53207e20,
                    "6d": 0.79310e20,
                    "6e": 0.93794e20,
                    "7b": 3.52719e20,
                    "9b": 2.69452e20,
                    "9c": 1.03679e20,
                    "9d": 5.15566e20 }
 
    def _set_osc_para(self):
        ## Neutrino oscillation parameters (taken from T2K-TN-367)
        L = 295.             # baseline [km]
        sinth13  = 0.0211    # sin^2(theta_13) with reactor constraint
        sin2th13 = 4. * sinth13 * ( 1. - sinth13 )
        sinth23  = 0.541     # sin^2(theta_23)
        sin2th23 = 4. * sinth23 * ( 1. - sinth23 )
        osca = sin2th13 * sinth23
        oscb = (( 1. - sinth13 ) ** 2) * sin2th23
        deltam32 = 2.469e-3  # (delta-m32)^2 in normal hierarchy
        return L, osca, oscb, deltam32

    def _set_nudir(self):
        # T2K neutrino beam direction
        nudir = [ 0.66976, -0.74218, 0.024223 ] 
        return nudir

    def _set_pot(self, run):
        ## P.O.T value in each run
        if run in self.pot:
            return self.pot[run]
        else:
            raise ValueError(f"Unknown anamode: {self.run_number}")

    def _set_ncel_scales(self):
        ## MC scale mode
        # - 1: Flux 11b; tuning v3.1/3.2 + NEUT 5.3.3; MDLQE = 22; CCQE 2p2h on
        # - 2: Flux 13a; tuning v3.0 FHC + NEUT 5.3.3; MDLQE = 22; CCQE 2p2h on
        # - 3: Flux 13a; tuning v3.0 RHC + NEUT 5.3.3; MDLQE = 22; CCQE 2p2h on
        # - 4: Flux 13a; tuning v4.0 FHC + NEUT 5.3.3; MDLQE = 22; CCQE 2p2h on
        # - 5: Flux 13a; tuning v4.0 RHC + NEUT 5.3.3; MDLQE = 22; CCQE 2p2h on
        # - 6: Flux 13a; tuning v4.0 FHC + NEUT 5.6.3; MDLQE = 22; CCQE 2p2h on
        if self.anamode == 1 :
            ncel_scales = { "numu"    : 2.55764e-18,
                            "nue"     : 5.04809e-20,
                            "numubar" : 7.96809e-20,
                            "nuebar"  : 4.57823e-21
                }
        elif self.anamode == 2 :
            ncel_scales = { "numu"    : 2.54405e-18,
                            "nue"     : 4.87431e-20,
                            "numubar" : 7.80696e-20,
                            "nuebar"  : 4.28773e-21
                }
        elif self.anamode == 3 :
            ncel_scales = { "numu"    : 3.49705e-19,
                            "nue"     : 1.46966e-20,
                            "numubar" : 6.08888e-19,
                            "nuebar"  : 1.06977e-20
                }
        elif self.anamode == 4 :
            ncel_scales = { "numu"    : 2.45100e-18,
                            "nue"     : 4.78849e-20,
                            "numubar" : 7.81700e-20,
                            "nuebar"  : 4.27219e-21
                }
        elif self.anamode == 5 :
            ncel_scales = { "numu"    : 3.54879e-19,
                            "nue"     : 1.47032e-20,
                            "numubar" : 5.86685e-19,
                            "nuebar"  : 1.04774e-20
                }
        elif self.anamode == 6 :
            ncel_scales = { "numu"    : 2.42246e-18,
                            "nue"     : 4.87745e-20,
                            "numubar" : 8.09021e-20,
                            "nuebar"  : 4.46683e-21
                }
        elif self.anamode == 7 : # take Run 11 value temporary
            ncel_scales = { "numu"    : 2.42246e-18,
                            "nue"     : 4.87745e-20,
                            "numubar" : 8.09021e-20,
                            "nuebar"  : 4.46683e-21
                }
        else :
            raise ValueError(f"Analysis mode {self.anamode} not found.")
        return ncel_scales

    def _set_fluxtune(self):
        # Flux 11b tuning v3.1/3.2 FHC
        if self.anamode == 1 :
            runs = [ "1", "2", "3b", "3c", "4" ]
            fluxdir = "/disk02/usr6/fiacob/ncgamma/SystematicErrors/beamweights/run1to4_11b_tunedv3.2"
            tunefiles = { "1"  : "sk_tuned11bv3.1_11anom_run1_fine.root",
                          "2"  : "sk_tuned11bv3.1_11anom_run2_fine.root",
                          "3b" : "sk_tuned11bv3.1_11anom_run3b_fine.root",
                          "3c" : "sk_tuned11bv3.1_11anom_run3c_fine.root",
                          "4"  : "sk_tuned11bv3.2_11anom_run4_fine.root"
                        }
            fluxtunes = defaultdict(dict)
            for run in runs :
                fluxtune = TFile( os.path.join( fluxdir, tunefiles[ run ] ) )
                fluxtunes[ run ][ "numu" ]          = fluxtune.Get( "enu_sk_tuned11b_numu_ratio" )
                fluxtunes[ run ][ "nue_x_numuflx" ] = fluxtune.Get( "enu_sk_tuned11b_numu_ratio" )
                fluxtunes[ run ][ "numubar" ]       = fluxtune.Get( "enu_sk_tuned11b_numub_ratio" )
                fluxtunes[ run ][ "nue" ]           = fluxtune.Get( "enu_sk_tuned11b_nue_ratio" )
                fluxtunes[ run ][ "nuebar" ]        = fluxtune.Get( "enu_sk_tuned11b_nueb_ratio" )
                for hist in fluxtunes[ run ].values() :
                    hist.SetDirectory( 0 )
        # Run1-9; Flux 13a tuning v3.0 (thin target) FHC
        elif self.anamode == 2 :
            runs = [ "1", "2", "3b", "3c", "4", "5a", "5b", "6a", "6f", "7a", "7c", "8", "9a" ]
            fluxdir = "/disk02/usr6/fiacob/ncgamma/SystematicErrors/beamweights/run1to9_fhc_13a_tunedv3.0"
            tunefiles = { "1"  : "sk_tuned13av3_13anom_run1_numode_fine.root",
                          "2"  : "sk_tuned13av3_13anom_run2_numode_fine.root",
                          "3b" : "sk_tuned13av3_13anom_run3b_numode_fine.root",
                          "3c" : "sk_tuned13av3_13anom_run3c_numode_fine.root",
                          "4"  : "sk_tuned13av3_13anom_run4_numode_fine.root",
                          "5a" : "sk_tuned13av3_13anom_run5a_numode_fine.root",
                          "5b" : "sk_tuned13av3_13anom_run5b_numode_fine.root",
                          "6a" : "sk_tuned13av3_13anom_run6a_numode_fine.root",
                          "6f" : "sk_tuned13av3_13anom_run6f_numode_fine.root",
                          "7a" : "sk_tuned13av3_13anom_run7a_numode_fine.root",
                          "7c" : "sk_tuned13av3_13anom_run7c_numode_fine.root",
                          "8"  : "sk_tuned13av3_13anom_run8_numode_fine.root",
                          "9a" : "sk_tuned13av3_13anom_run9a_numode_fine.root"
                        }
             
            fluxtunes = defaultdict(dict)
            for run in runs :
                fluxtune = TFile( os.path.join( fluxdir, tunefiles[ run ] ) )
                fluxtunes[ run ][ "numu" ]          = fluxtune.Get( "enu_sk_tuned13a_numu_ratio" )
                fluxtunes[ run ][ "nue_x_numuflx" ] = fluxtune.Get( "enu_sk_tuned13a_numu_ratio" )
                fluxtunes[ run ][ "numubar" ]       = fluxtune.Get( "enu_sk_tuned13a_numub_ratio" )
                fluxtunes[ run ][ "nue" ]           = fluxtune.Get( "enu_sk_tuned13a_nue_ratio" )
                fluxtunes[ run ][ "nuebar" ]        = fluxtune.Get( "enu_sk_tuned13a_nueb_ratio" )
                for hist in fluxtunes[ run ].values() :
                    hist.SetDirectory( 0 )
        
        # Run1-9; Flux 13a tuning v3.0 (thin target) RHC
        elif self.anamode == 3 :
            runs = [ "5c", "6b", "6c", "6d", "6e", "7b", "9b", "9c", "9d" ]
            fluxdir = "/disk02/usr6/fiacob/ncgamma/SystematicErrors/beamweights/run1to9_fhc_13a_tunedv3.0"
            tunefiles = { "5c" : "sk_tuned13av3_13anom_run5c_antinumode_fine.root",
                          "6b" : "sk_tuned13av3_13anom_run6b_antinumode_fine.root",
                          "6c" : "sk_tuned13av3_13anom_run6c_antinumode_fine.root",
                          "6d" : "sk_tuned13av3_13anom_run6d_antinumode_fine.root",
                          "6e" : "sk_tuned13av3_13anom_run6e_antinumode_fine.root",
                          "7b" : "sk_tuned13av3_13anom_run7b_antinumode_fine.root",
                          "9b" : "sk_tuned13av3_13anom_run9b_antinumode_fine.root",
                          "9c" : "sk_tuned13av3_13anom_run9c_antinumode_fine.root",
                          "9d" : "sk_tuned13av3_13anom_run9d_antinumode_fine.root"
                        }
            #
            fluxtunes = defaultdict(dict)
            for run in runs :
                fluxtune = TFile( os.path.join( fluxdir, tunefiles[ run ] ) )
                fluxtunes[ run ][ "numu" ]          = fluxtune.Get( "enu_sk_tuned13a_numu_ratio" )
                fluxtunes[ run ][ "nue_x_numuflx" ] = fluxtune.Get( "enu_sk_tuned13a_numu_ratio" )
                fluxtunes[ run ][ "numubar" ]       = fluxtune.Get( "enu_sk_tuned13a_numub_ratio" )
                fluxtunes[ run ][ "nue" ]           = fluxtune.Get( "enu_sk_tuned13a_nue_ratio" )
                fluxtunes[ run ][ "nuebar" ]        = fluxtune.Get( "enu_sk_tuned13a_nueb_ratio" )
                for hist in fluxtunes[ run ].values() :
                    hist.SetDirectory( 0 )
        
        # Run1-9; Flux 13a tuning v4.0 (reprica target) FHC
        elif self.anamode == 4 :
            runs = [ "1", "2", "3b", "3c", "4", "5a", "5b", "6a", "6f", "7a", "7c", "8", "9a"]
            fluxdir = "/disk02/usr6/fiacob/ncgamma/SystematicErrors/beamweights/run1to9_fhc_13a_tunedv4.0"
            tunefiles = { "1"  : "sk_tuned13av4_13anom_run1_numode_fine.root",
                          "2"  : "sk_tuned13av4_13anom_run2_numode_fine.root",
                          "3b" : "sk_tuned13av4_13anom_run3b_numode_fine.root",
                          "3c" : "sk_tuned13av4_13anom_run3c_numode_fine.root",
                          "4"  : "sk_tuned13av4_13anom_run4_numode_fine.root",
                          "5a" : "sk_tuned13av4_13anom_run5a_numode_fine.root",
                          "5b" : "sk_tuned13av4_13anom_run5b_numode_fine.root",
                          "6a" : "sk_tuned13av4_13anom_run6a_numode_fine.root",
                          "6f" : "sk_tuned13av4_13anom_run6f_numode_fine.root",
                          "7a" : "sk_tuned13av4_13anom_run7a_numode_fine.root",
                          "7c" : "sk_tuned13av4_13anom_run7c_numode_fine.root",
                          "8"  : "sk_tuned13av4_13anom_run8_numode_fine.root",
                          "9a" : "sk_tuned13av4_13anom_run9a_numode_fine.root"
                        }
            #
            fluxtunes = defaultdict(dict)
            for run in runs :
                fluxtune = TFile( os.path.join( fluxdir, tunefiles[ run ] ) )
                fluxtunes[ run ][ "numu" ]          = fluxtune.Get( "enu_sk_tuned13a_numu_ratio" )
                fluxtunes[ run ][ "nue_x_numuflx" ] = fluxtune.Get( "enu_sk_tuned13a_numu_ratio" )
                fluxtunes[ run ][ "numubar" ]       = fluxtune.Get( "enu_sk_tuned13a_numub_ratio" )
                fluxtunes[ run ][ "nue" ]           = fluxtune.Get( "enu_sk_tuned13a_nue_ratio" )
                fluxtunes[ run ][ "nuebar" ]        = fluxtune.Get( "enu_sk_tuned13a_nueb_ratio" )
                for hist in fluxtunes[ run ].values() :
                    hist.SetDirectory( 0 )
        
        # Run1-9; Flux 13a tuning v4.0 (reprica target) RHC
        elif self.anamode == 5 :
            runs = [ "5c", "6b", "6c", "6d", "6e", "7b", "9b", "9c", "9d" ]
            fluxdir = "/disk02/usr6/fiacob/ncgamma/SystematicErrors/beamweights/run1to9_rhc_13a_tunedv4.0"
            tunefiles = { "5c" : "sk_tuned13av4_13anom_run5c_antinumode_fine.root",
                          "6b" : "sk_tuned13av4_13anom_run6b_antinumode_fine.root",
                          "6c" : "sk_tuned13av4_13anom_run6c_antinumode_fine.root",
                          "6d" : "sk_tuned13av4_13anom_run6d_antinumode_fine.root",
                          "6e" : "sk_tuned13av4_13anom_run6e_antinumode_fine.root",
                          "7b" : "sk_tuned13av4_13anom_run7b_antinumode_fine.root",
                          "9b" : "sk_tuned13av4_13anom_run9b_antinumode_fine.root",
                          "9c" : "sk_tuned13av4_13anom_run9c_antinumode_fine.root",
                          "9d" : "sk_tuned13av4_13anom_run9d_antinumode_fine.root",
                        }
            #
            fluxtunes = defaultdict(dict)
            for run in runs :
                fluxtune = TFile( os.path.join( fluxdir, tunefiles[ run ] ) )
                fluxtunes[ run ][ "numu" ]          = fluxtune.Get( "enu_sk_tuned13a_numu_ratio" )
                fluxtunes[ run ][ "nue_x_numuflx" ] = fluxtune.Get( "enu_sk_tuned13a_numu_ratio" )
                fluxtunes[ run ][ "numubar" ]       = fluxtune.Get( "enu_sk_tuned13a_numub_ratio" )
                fluxtunes[ run ][ "nue" ]           = fluxtune.Get( "enu_sk_tuned13a_nue_ratio" )
                fluxtunes[ run ][ "nuebar" ]        = fluxtune.Get( "enu_sk_tuned13a_nueb_ratio" )
                for hist in fluxtunes[ run ].values() :
                    hist.SetDirectory( 0 )
          
        # Run11; Flux 21b tuning v2.0 (reprica target) FHC
        elif self.anamode == 6 :
            runs = [ "11" ]
            fluxdir = "/disk02/usr7/licheng/SK/ncgamma/ncqeana/selection/Macro/T2KFlux"
            tunefiles = { "11" : "sk_tuned21bv2_13anom_run11_numode_fine.root"}
            #
            fluxtunes = defaultdict(dict)
            for run in runs :
                fluxtune = TFile( os.path.join( fluxdir, tunefiles[ run ] ) )
                fluxtunes[ run ][ "numu" ]          = fluxtune.Get( "enu_sk_tuned21b_numu_ratio" )
                fluxtunes[ run ][ "nue_x_numuflx" ] = fluxtune.Get( "enu_sk_tuned21b_numu_ratio" )
                fluxtunes[ run ][ "numubar" ]       = fluxtune.Get( "enu_sk_tuned21b_numub_ratio" )
                fluxtunes[ run ][ "nue" ]           = fluxtune.Get( "enu_sk_tuned21b_nue_ratio" )
                fluxtunes[ run ][ "nuebar" ]        = fluxtune.Get( "enu_sk_tuned21b_nueb_ratio" )
                for hist in fluxtunes[ run ].values() :
                    hist.SetDirectory( 0 )

        # Run10; Temporary take Run 9 setting
        elif self.anamode == 7 :
            runs = [ "10a", "10b" ]
            fluxdir = "/disk02/usr6/fiacob/ncgamma/SystematicErrors/beamweights/run1to9_fhc_13a_tunedv4.0"
            tunefiles = { "10a" : "sk_tuned13av4_13anom_run9a_numode_fine.root",
                          "10b" : "sk_tuned13av4_13anom_run9a_numode_fine.root"
                        }
            #
            fluxtunes = defaultdict(dict)
            for run in runs :
                fluxtune = TFile( os.path.join( fluxdir, tunefiles[ run ] ) )
                fluxtunes[ run ][ "numu" ]          = fluxtune.Get( "enu_sk_tuned13a_numu_ratio" )
                fluxtunes[ run ][ "nue_x_numuflx" ] = fluxtune.Get( "enu_sk_tuned13a_numu_ratio" )
                fluxtunes[ run ][ "numubar" ]       = fluxtune.Get( "enu_sk_tuned13a_numub_ratio" )
                fluxtunes[ run ][ "nue" ]           = fluxtune.Get( "enu_sk_tuned13a_nue_ratio" )
                fluxtunes[ run ][ "nuebar" ]        = fluxtune.Get( "enu_sk_tuned13a_nueb_ratio" )
                for hist in fluxtunes[ run ].values() :
                    hist.SetDirectory( 0 )
        
        else :
            raise ValueError(f"Analysis mode {self.anamode} not found.")
        return runs, fluxtunes









        


