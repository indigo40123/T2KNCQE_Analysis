from ROOT import TH1D

class NCQE_Neutron_Histo:

    def __init__(self):
        # Define selection, cut, and interaction names
        self.catagories = ["all", "Gd", "H", "Noise"]
        self.cutnames = ["angle"]
        #self.cutnames = ["nocut", "postact", "wallfv", "dwall", "effwall", "ovaq", "angle"]
        self.intnames = ["all", "nuncqe", "nubarncqe", "nc1pi", "ncother", "ccqe", "ccqe2p2h", "ccother", "others"]

        # Define feature properties (name, x-axis label, binning)
        self.features = [
            {"name": "hntag_Tds",    "label": "Capture time[#mus]",    "bins": ( 6,    0.0,  600.0)},
            {"name": "hntag_Dist",   "label": "Travel distance [cm]",  "bins": (15,    0.0, 1500.0)},
            {"name": "hntag_BeamCos","label": "Cos#theta_{n#b}",       "bins": ( 5,   -1.0,    1.0)},
            {"name": "hntag_GaCos",  "label": "Cos#theta_{n#gamma}",   "bins": ( 5,   -1.0,    1.0)},
            {"name": "hntag_DistL",  "label": "Longtitual dist. [cm]", "bins": (13, -650.0,  650.0)},
            {"name": "hntag_DistT",  "label": "Transverse dist. [cm]", "bins": (16,    0.0, 1600.0)},
            {"name": "hntag_x",      "label": "X_n [m]",               "bins": ( 5,  -20.0,   20.0)},
            {"name": "hntag_y",      "label": "Y_n [m]",               "bins": ( 5,  -20.0,   20.0)},
            {"name": "hntag_z",      "label": "Z_n [m]",               "bins": ( 5,  -18.0,   18.0)},
            {"name": "hntag_r2",     "label": "R^2_n [m^2]",           "bins": ( 7,    0.0,  280.0)}
        ]

        self.featuresNN = [ 
            {"name": "hntag_NHits",     "label": "NHits",               "bins": (30,    0.0,   60.0)},
            {"name": "hntag_NResHits",  "label": "NResHits",            "bins": (40,    0.0,   80.0)},
            {"name": "hntag_TRMS",      "label": "TRMS     [ns]",       "bins": (20,    0.0,   10.0)},
            {"name": "hntag_DWall",     "label": "DWall    [cm]",       "bins": (20, -400.0, 1600.0)},
            {"name": "hntag_DWallDir",  "label": "DWallDir [cm]",       "bins": (20,    0.0, 5000.0)},
            {"name": "hntag_B1",        "label": "Beta 1",              "bins": (20,   -0.4,    1.0)},
            {"name": "hntag_B2",        "label": "Beta 2",              "bins": (70,   -0.4,    1.0)},
            {"name": "hntag_B3",        "label": "Beta 3",              "bins": (70,   -0.4,    1.0)},
            {"name": "hntag_B4",        "label": "Beta 4",              "bins": (70,   -0.4,    1.0)},
            {"name": "hntag_B5",        "label": "Beta 5",              "bins": (70,   -0.4,    1.0)},
            {"name": "hntag_AngleMean", "label": "AngleMean [deg]",     "bins": (30,   20.0,   80.0)},
            {"name": "hntag_AngleSkew", "label": "AngleSkew [deg]",     "bins": (50, -150.0,  150.0)},
            {"name": "hntag_AngleStdev","label":"AngleStedv[deg]",      "bins": (40,   10.0,   30.0)},
            {"name": "hntag_DirAngleMean","label":"DirAngleMean[deg]",  "bins": (35,   20.0,   90.0)},
            {"name": "hntag_DirAngleRMS", "label":"DirAngleRMS[deg]",   "bins": (30,    0.0,   60.0)},
            {"name": "hntag_BRatio",    "label":"Brust Ratio",          "bins": (20,    0.0,    1.0)},
            {"name": "hntag_FitGood",   "label":"Fit Goodness",         "bins": (40,    0.0,    1.0)},
            {"name": "hntag_DarkLikl",  "label":"Dark Likelihood",      "bins": (20,    0.0,    1.0)},
            {"name": "hntag_TagOut",    "label":"NN TagOut",            "bins": (20,    0.0,    1.0)}
        ]

        # Initialize dictionaries for histograms
        self.histograms = {}
        self.histogramsNN = {}

        # Call the method to set up the histograms
        self._initialize_histograms()
        self._initialize_histogramsNN()

    def _initialize_histograms(self):
        """
        Initialize histograms and store them in the dictionaries.
        """
        for feature in self.features:
            feature_name  = feature["name"]
            feature_label = feature["label"]
            feature_bins  = feature["bins"]

            # Initialize the feature in the histogram dictionary
            self.histograms[feature_name] = {}

            for catagory in self.catagories:
                self.histograms[feature_name][catagory] = {}
                for cutname in self.cutnames:
                    self.histograms[feature_name][catagory][cutname] = {}
                    for intname in self.intnames:
                        # Construct the histogram name
                        hist_name = "_".join([feature_name, catagory, cutname, intname])
                        self.histograms[feature_name][catagory][cutname][intname] = \
                            TH1D(hist_name, f"; {feature_label}; Events", *feature_bins)

    def _initialize_histogramsNN(self):
        """
        Initialize NN histograms and store them in the dictionaries.
        """
        for feature in self.featuresNN:
            feature_name  = feature["name"]
            feature_label = feature["label"]
            feature_bins  = feature["bins"]

            # Initialize the feature in the histogram dictionary
            self.histogramsNN[feature_name] = {}

            for catagory in self.catagories:
                self.histogramsNN[feature_name][catagory] = {}
                for cutname in self.cutnames:
                    # Construct the histogram name
                    hist_name = "_".join([feature_name, catagory, cutname])
                    self.histogramsNN[feature_name][catagory][cutname] = \
                        TH1D(hist_name, f"; {feature_label}; Events", *feature_bins)


    def get_histogram(self, feature_name, catagory, cutname, intname):
        """
        Returns the requested TH1D histogram based on feature_name, catagory, cutname, and intname.
        """
        return self.histograms[feature_name][catagory][cutname][intname]

    def get_histogramNN(self, feature_name, catagory, cutname):
        """
        Returns the requested TH1D histogram based on feature_name, catagory, cutname for NN feaature.
        """
        return self.histogramsNN[feature_name][catagory][cutname]

