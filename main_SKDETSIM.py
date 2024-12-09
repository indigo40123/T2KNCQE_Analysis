#!/usr/bin/python
#------------------------------------------------------------------------------
#  T2K NCQE analysis code, inherited from numerous predecessors.
#  Last updated by LiCheng FENG on December 7, 2024.
#------------------------------------------------------------------------------

import sys
from optparse import OptionParser
from glob import glob
from math import sin
from math import sqrt
import progressbar as pb
import ROOT
from ROOT import TFile, TH1F, TH1D, TH2D, TH1, TChain

from T2K_Config import *
from NCQE_Cut import *
from NCQE_Tree import *
from NCQE_Gamma_Hist import *
from NCQE_Neutron_Hist import *

def parse():
    #------------------------------------------------------------------------------
    usage = "usage: %prog [options] infiles1 infiles2 ..."
    parser = OptionParser( usage = usage )
    # Add options
    parser.add_option("-o", "--histOutputName",
                      dest="outHistFile", default="ncqe_SKDThistogram_mc.root", metavar="FILE",
                      help="Output ROOT filename for histogram (default: %(default)s)")
    parser.add_option("-t", "--mcOutName",
                      dest="outmcFile", default="ncqe_SKDTselected_mc.root", metavar="FILE",
                      help="Output ROOT filename for TTree (default: %(default)s)")
    parser.add_option("-f", "--friend",
                      dest="frienddir",   default="", metavar="DIR",
                      help="Directory containing friend trees. Only used in MC mode.")
    # Parse the arguments
    ( options, args ) = parser.parse_args()
    # Add '-b' option to sys.argv
    sys.argv.append("-b")
    # Start of the program logic
    print("*** START OF PROGRAM ***")
    print("Input files:", args)
    print("Output histogram file:", options.outHistFile)
    print("Output mc file:", options.outmcFile)

    #------------------------------------------------------------------------------
    # Group files is there are many
    groupedFiles = defaultdict( list )
    friendFiles = False
    # Input file name example
    # File name = lentp_nuebar.ncgamma_flux13a_neut533.030.root
    # Split with ".", [lentp_nuebar, ncgamma_flux13a_neut533, 030, root]
    # Split with "-", [lentp, nuebar, ncgamma, flux13a, neut533, 030, root]
    # Choose the [1] element, the neutrion flavor info.

    print ("*** Extract Input FILENAMES ***")
    for arg in args :  # Iterate through arguments
        for fname in glob( arg ) :  # Get files in directory arg
            ftle = os.path.basename( fname ).split( "." )[ 0 ]
            ft = ftle.split( "_" )[ 1 ]  # get neutrino flavor
            groupedFiles[ ft ] += [ fname ]

    if len( groupedFiles ) == 0 :
        print ("Input MC files needed!")
        sys.exit(2)

    return groupedFiles, options

    
def main():

    # access file list from I/O parse interface
    groupedFiles, options = parse()

    # load T2K Setting
    # Including Run, Oscillation, POT, Xsec, parameter... etc
    t2k = T2K(anamode=6)
    ncqe_cut = NCQE_Cut(run = 11, anamode = 6)
    n_gen = 100*1000

    # Initialize NCQE Tree to save selected mc value in the "ncqe_fullinfo_mc.root" file
    NCQE_selected = NCQE__mc(filename=options.outmcFile,
                                  treename="NCQETree",
                                  title="selected T2K NCQE MC")

    # Initialize gamma histograms for "ncqe_histogram_mc.root" file
    hist_gamma = NCQE_Gamma_Histo()

    # Create histograms for gammas features (e.g., 'herec', 'hdwall' ... etc)
    for feature in hist_gamma.features:              # Loop over features
        feature_name = feature["name"]               # Get the feature name
        for selname in hist_gamma.selnames:          # Loop over signal names
            for cutname in hist_gamma.cutnames:      # Loop over cuts
                for intname in hist_gamma.intnames:  # Loop over interaction 
                    # Access the histogram for this combination
                    histogram = hist_gamma.get_histogram(feature_name, selname, cutname, intname)
                    # Create a variable name using the pattern: [feature][selname][cutname][intname]
                    variable_name = f"{feature_name}_{selname}_{cutname}_{intname}"
                    # Dynamically assign the variable in the global scope 
                    globals()[variable_name] = histogram

    # Initialize neutron histograms for "ncqe_histogram_mc.root" file
    hist_neutron = NCQE_Neutron_Histo()
    # Create histograms for neutron features (e.g.,'Tds', 'Dist', 'Vertex', ... etc)
    for feature in hist_neutron.features:                # Loop over neutron features
        feature_name = feature["name"]                   # Get the feature name
        for cutname in hist_neutron.cutnames:            # Loop over NCQE cut types
            for catagory in hist_neutron.catagories:     # Loop over all n-cap types
                for intname in hist_neutron.intnames:    # Loop over interaction
                    # Create Neutron basic histogram (w/ interaction channel) 
                    histogram = hist_neutron.get_histogram(feature_name, catagory, cutname, intname)
                    variable_name = f"{feature_name}_{catagory}_{cutname}_{intname}"
                    globals()[variable_name] = histogram

    # Create histograms for neutron NN features (e.g.,'NHits', 'Angle', 'TagOut', ... etc)     
    for feature in hist_neutron.featuresNN:             # Loop over NN features
        feature_name = feature["name"]                   # Get the feature name
        for cutname in hist_neutron.cutnames:            # Loop over NCQE cut types
            for catagory in hist_neutron.catagories:     # Loop over all n-cap types
                # Create Neutron NN histogram (w/o interaction channel)
                histogram_NN = hist_neutron.get_histogramNN(feature_name, catagory, cutname)
                variable_nameNN = f"{feature_name}_{catagory}_{cutname}"
                globals()[variable_nameNN] = histogram_NN
    
    ### process input MC files ###
    for fileType, infiles in groupedFiles.items() :
        # define TChain and add trees from MC files
        mctree  = TChain( "h1")        #For ntuple tree, add prompt info
        mctree1 = TChain( "event")     #For NTag, Nmulti info
        mctree2 = TChain( "taggable")  #For NTag, NTaggable detail
        mctree3 = TChain( "ntag")      #For NTag, NTagged detail
    
        # Add up all the input file
        for infile in infiles :
            mctree.Add( infile )
            mctree1.Add( infile )
            mctree2.Add( infile )
            mctree3.Add( infile )

        # get TChain entries
        maxev = mctree.GetEntries()
        print("Begin processing for", mctree.GetNtrees(), fileType, "files")
 
        # set up the progress bar
        widgets = [ 'Events: ', 
                    pb.Percentage(), ' ',
                    pb.Bar( marker = '=', left = '[', right = ']' ), ' ', 
                    pb.ETA() ]
        pbar = pb.ProgressBar( widgets = widgets, maxval = maxev, term_width = 80 )
        pbar.start()
        print("")

        ### loop over all event entries ###
        for iev in range( maxev ) :
            pbar.update(iev)
            mctree.GetEntry(iev)
            mctree1.GetEntry(iev)
            mctree2.GetEntry(iev)
            mctree3.GetEntry(iev)
            # Features
            enu      = mctree.pnu[0]    # nu energy [MeV]
            erec_org = mctree.erec      # bsenergy  [MeV]
            erec     = erec_org - 0.51  # visible energy [MeV]
            dwall    = mctree.wall      # dwall   [cm]
            effwall  = mctree.effwall   # effwall [cm]
            ovaq     = mctree.ovaq      # ovaQ    [arb]
            angle    = mctree.angle     # Cherenkov angle [degree]
            # Bonsai Vertex
            pos_x    = mctree.pos[0]/100  # [m]    
            pos_y    = mctree.pos[1]/100  # [m]
            pos_z    = mctree.pos[2]/100  # [m] 
            pos_r2   = (pos_x*pos_x + pos_y*pos_y)  # Radiusi squre [m^2]
            # MC truth Vertex
            posvx    = mctree.posv[0]/100 # [m] 
            posvy    = mctree.posv[1]/100 # [m]
            posvz    = mctree.posv[2]/100 # [m]
            # Bonsai Direction 
            bdir_x   = mctree.bdir[0] 
            bdir_y   = mctree.bdir[1]
            bdir_z   = mctree.bdir[2]
            cosb     = bdir_x*t2k.nudir[0] + bdir_y*t2k.nudir[1] + bdir_z*t2k.nudir[2]
            #Neutron multiplicity info
            Ntrue    = mctree1.NTrueN     # MC truth Nmulti
            Ntaggable= mctree1.NTaggableN # Pre-selection NMulti
            Ntagged  = mctree1.NTaggedN   # NN-selected Nmulti

            # Place NCQE selection and check channel
            is_ncq_event = ncqe_cut.is_NCQE(erec, dwall, effwall, ovaq, angle) 
            interaction  = ncqe_cut.channel(mctree.Neutmode)
            if not is_ncq_event :
                continue

            ### Fill NCQE mc info into TTree
            NCQE_selected.fill( enu, erec, dwall, effwall, ovaq, angle, \
                                pos_x, pos_y, pos_z, pos_r2, posvx, posvy, posvz, \
                                bdir_x, bdir_y, bdir_z, cosb, Ntrue, Ntaggable, Ntagged )


            ###################################################
            # Access Neutron Tagging details from here
            ###################################################
            #
            # Define dictionaries for saving neutron info
            label_map    = { 0: 'Noise', 2: 'H', 3: 'Gd' }
            categories   = ['all', 'Gd', 'H', 'Noise']

            # Variable name in NTag Output
            n_in_NTag   = ['FitT', 'DPrompt', 'beamcos', 'gammacos', \
                           'DistL', 'DistT', 'fvx', 'fvy', 'fvz', 'r2']
            
            # Variable name in NTag Output
            nNN_in_NTag = ['NHits', 'NResHits', 'TRMS',  'DWall', 'DWallMeanDir',\
                           'Beta1', 'Beta2',    'Beta3', 'Beta4', 'Beta5',\
                           'OpeningAngleMean','OpeningAngleSkew','OpeningAngleStdev',\
                           'MeanDirAngleMean','MeanDirAngleRMS',\
                           'BurstRatio','FitGoodness','DarkLikelihood', 'TagOut']
           
            # Match neutron variable name with histogram name
            nfeature_mapping = {'FitT': 'hntag_Tds', 'DPrompt': 'hntag_Dist',
                                'beamcos' : 'hntag_BeamCos',
                                'gammacos': 'hntag_GaCos',
                                'DistL' : 'hntag_DistL',
                                'DistT' : 'hntag_DistT',
                                'fvx': 'hntag_x', 'fvy': 'hntag_y',
                                'fvz': 'hntag_z',  'r2': 'hntag_r2' }

            # Match neutron NN variable name with histogram name
            nfeatureNN_mapping = {'NHits': 'hntag_NHits', 'NResHits': 'hntag_NResHits',
                                  'TRMS' : 'hntag_TRMS',  'DWall' : 'hntag_DWall',
                                  'DWallMeanDir': 'hntag_DWallDir', 'Beta1': 'hntag_B1',
                                  'Beta2': 'hntag_B2', 'Beta3': 'hntag_B3',
                                  'Beta4': 'hntag_B4', 'Beta5': 'hntag_B5',
                                  'OpeningAngleMean': 'hntag_AngleMean',
                                  'OpeningAngleSkew': 'hntag_AngleSkew',
                                  'OpeningAngleStdev':'hntag_AngleStdev',
                                  'MeanDirAngleMean': 'hntag_DirAngleMean',
                                  'MeanDirAngleRMS':  'hntag_DirAngleRMS',
                                  'BurstRatio': "hntag_BRatio",
                                  'FitGoodness':"hntag_FitGood",
                                  'DarkLikelihood':"hntag_DarkLikl",
                                  'TagOut':"hntag_TagOut"}

            # Initialize dictionaries to hold neutron info
            n_feature = {}
            for feature in n_in_NTag:
                n_feature[feature] = {}
                for category in categories:
                    n_feature[feature][category] = []
            
            n_featureNN = {}
            for feature in nNN_in_NTag:
                n_featureNN[feature] = {}
                for category in categories:
                    n_featureNN[feature][category] = []
            
            ### Loop over the NN candidates event info ###
            Neutron_candi = int(mctree1.NCandidates)
            for i in range( 0, Neutron_candi ) :
                if (mctree3.TagOut[i] > 0.7):
                    # neutron direction are not included in NTag, calculated here  
                    ndir = n_dir(mctree3.fvx[i]/100, mctree3.fvy[i]/100, mctree3.fvz[i]/100, pos_x, pos_y, pos_z)
                    n_gammacos = ndir[0]*bdir_x + ndir[1]*bdir_y + ndir[2]*bdir_z
                    n_beamcos  = ndir[0]*t2k.nudir[0] + ndir[1]*t2k.nudir[1] + ndir[2]*t2k.nudir[2]
                    n_distlong = mctree3.DPrompt[i] * n_beamcos
                    n_disttran = mctree3.DPrompt[i] * n_gammacos
                    n_r2 = r2(mctree3.fvx[i], mctree3.fvy[i])
                    feature_map = {'beamcos': n_beamcos, 'gammacos': n_gammacos,
                                   'DistL': n_distlong,  'DistT': n_disttran, 'r2': n_r2 }
                    # Get the truth n classification catagory
                    category = label_map.get(mctree3.Label[i])
                    # Check if vaild capture or noise
                    if category:
                        for feature in n_in_NTag:
                            # Get and Fill the neutron info
                            if feature in feature_map:
                                value = feature_map[feature]
                            else:
                                value = getattr(mctree3, feature)[i]
                            n_feature[feature]['all'].append(value)
                            n_feature[feature][category].append(value)

                        for featureNN in nNN_in_NTag:
                            # Get and fill the neutron NN info
                            valueNN = getattr(mctree3, featureNN)[i]
                            n_featureNN[featureNN]['all'].append(valueNN)
                            n_featureNN[featureNN][category].append(valueNN)

                    # Sample code to check if the wanted parameter are recored
                    #print("Neutron    tds: ", n_feature['FitT']['all'])
                    #print("Neutron-Gd tds: ", n_feature['FitT']['Gd'])
                    #print("Neutron    NHis: ", n_featureNN['NHits']['all'])
                    #print("Neutron-Gd NHis: ", n_featureNN['NHits']['Gd'])

            
            # Calculate the neutrino oscillation probability
            pmutoe  = t2k.osca * (sin( 1.267 * t2k.deltam32 * t2k.L / enu) ** 2 )
            pmutomu = 1. - ( t2k.oscb + t2k.osca ) * \
                           ( sin( 1.267 * t2k.deltam32 * t2k.L / enu) ** 2 )
            posc = pmutoe + pmutomu
            
            ### loop over selected runs with pre-calculated weight ###
            for run in t2k.runs :
                ## weight
                wgt = 1.0
                wgt = t2k.ncel_scales[ fileType ] * t2k.pot[ run ] / (n_gen)
                if fileType in t2k.fluxtunes[ run ] :
                    ibin = t2k.fluxtunes[ run ][ fileType ].FindFixBin( enu )
                    wgt *= t2k.fluxtunes[ run ][ fileType ].GetBinContent( ibin )

                variables = [enu, erec, dwall, effwall, ovaq, angle, cosb, \
                             pos_x, pos_y, pos_z, pos_r2, \
                             Ntrue, Ntaggable, Ntagged]
                
                # Fill NCQE gamma info into histograms
                for var, feature in zip(variables, hist_gamma.features):
                    feature_name = feature["name"]
                    hist_gamma.histograms[feature_name]["ncgamma"]["angle"][interaction].Fill(var, wgt)
                    hist_gamma.histograms[feature_name]["ncgamma"]["angle"]["all"].Fill(var, wgt) 

                # Fill NCQE neutron info into histogram
                for n_record in n_feature:
                    feature_name = nfeature_mapping.get(n_record)
                    if feature_name is None:
                        print(f"No matching feature found for {n_record}")
                        continue

                    for category in n_feature[n_record]:
                        values = n_feature[n_record][category]
                        for value in values:
                            hist_neutron.histograms[feature_name][category]["angle"][interaction].Fill(value, wgt)
                            hist_neutron.histograms[feature_name][category]["angle"]["all"].Fill(value, wgt)

                # Fill NCQE neutron NN info into histogram
                for n_record in n_featureNN:
                    feature_name = nfeatureNN_mapping.get(n_record)
                    if feature_name is None:
                        print(f"No matching feature found for {n_record}")
                        continue

                    for category in n_featureNN[n_record]:
                        values = n_featureNN[n_record][category]
                        for value in values:
                            hist_neutron.histogramsNN[feature_name][category]["angle"].Fill(value, wgt)
                            hist_neutron.histogramsNN[feature_name][category]["angle"].Fill(value, wgt) 


    ### Write histograms to "ncqe_fullinfo_mc.root" ###
    fout = TFile(options.outmcFile, "RECREATE")
    fout.cd()
    NCQE_selected.tree.Write()
    fout.Close()

    ### Write histograms to "ncqe_histogram_mc.root" ###
    fout = TFile(options.outHistFile, "RECREATE")
    fout.cd()
    for feature in hist_gamma.features:
        feature_name = feature["name"]
        for channel in hist_gamma.intnames:
            hist_gamma.histograms[feature_name]["ncgamma"]["angle"][channel].Write()

    for feature in hist_neutron.features:
        feature_name = feature["name"]
        for category in hist_neutron.catagories:
            for channel in hist_neutron.intnames:
                hist_neutron.histograms[feature_name][category]["angle"][channel].Write()
                continue # Uncomment to show the neutron info histogram in the output file

    for feature in hist_neutron.featuresNN:
        feature_name = feature["name"]
        for category in hist_neutron.catagories:
            #hist_neutron.histogramsNN[feature_name][category]["angle"].Write()
            continue # Uncomment to show the neutron NN histogram in the output file
    fout.Close()

    pbar.finish()
    print("*** END OF PROGRAM ***")


def n_dir( fvx, fvy, fvz, pfvx, pfvy, pfvz ):
    diff = [fvx - pfvx, fvy - pfvy, fvz - pfvz]
    vecmod = sqrt(sum(d ** 2 for d in diff))
    return [d / vecmod for d in diff]

def r2( fvx, fvy): # input cm, output m
    return (fvx/100)**2 + (fvy/100)**2

if __name__ == "__main__":
    main()
