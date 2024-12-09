from ROOT import TH1D

class NCQE_Gamma_Histo:
    def __init__(self):
        # Define selection, cut, and interaction names
        self.selnames = ["ncgamma"]
        self.cutnames = ["angle"]
        #self.cutnames = ["nocut", "postact", "wallfv", "dwall", "effwall", "ovaq", "angle"]
        self.intnames = ["all", "nuncqe", "nubarncqe", "nc1pi", "ncother", "ccqe", "ccqe2p2h", "ccother", "others"]

        # Define feature properties (name, x-axis label, binning)
        self.features = [
            {"name": "henu",     "label": "E_{#nu} [GeV]",   "bins": (200,   0.00,   10.00)},
            {"name": "herec",    "label": "E_{rec} [GeV]",   "bins": ( 26,   3.49,   29.49)},
            {"name": "hdwall",   "label": "dwall [cm]",      "bins": ( 16, 200.00, 1800.00)},
            {"name": "heffwall", "label": "effwall [cm]",    "bins": ( 23, 200.00, 4800.00)},
            {"name": "hovaq",    "label": "OvaQ",            "bins": ( 24,  -0.40,    0.80)},
            {"name": "hangle",   "label": "#theta_{c} [deg]","bins": ( 33,   0.00,   90.00)},
            {"name": "hcosb",    "label": "#theta_{beam}",   "bins": ( 10,  -1.00,    1.00)},
            {"name": "hx",       "label": "X [cm]",          "bins": (  5, -20.00,   20.00)},
            {"name": "hy",       "label": "Y [cm]",          "bins": (  5, -20.00,   20.00)},
            {"name": "hz",       "label": "Z [cm]",          "bins": (  5, -16.50,   16.50)},
            {"name": "hr2",      "label": "R^2 [cm]",        "bins": (  5,   0.00,  220.00)},
            {"name": "htrue_n",  "label": "True MultiN",     "bins": ( 15,  -0.50,   14.50)},
            {"name": "htaggable_n","label":"Taggable MultiN","bins": ( 15,  -0.50,   14.50)},
            {"name": "htagged_n",  "label":"Tagged MultiN",  "bins": ( 15,  -0.50,   14.50)}
        ]

        # Initialize dictionaries for histograms
        self.histograms = {}

        # Call the method to set up the histograms
        self._initialize_histograms()

    def _initialize_histograms(self):
        """
        Initialize histograms and store them in the dictionaries.
        """
        for feature in self.features:
            feature_name = feature["name"]
            feature_label = feature["label"]
            feature_bins = feature["bins"]

            # Initialize the feature in the histogram dictionary
            self.histograms[feature_name] = {}

            for selname in self.selnames:
                self.histograms[feature_name][selname] = {}
                for cutname in self.cutnames:
                    self.histograms[feature_name][selname][cutname] = {}
                    for intname in self.intnames:
                        # Construct the histogram name
                        hist_name = "_".join([feature_name, selname, cutname, intname])
                        self.histograms[feature_name][selname][cutname][intname] = \
                            TH1D(hist_name, f"; {feature_label}; Events", *feature_bins)

    def get_histogram(self, feature_name, selname, cutname, intname):
        """
        Returns the requested histogram based on feature_name, selname, cutname, and intname.
        """
        return self.histograms[feature_name][selname][cutname][intname]

