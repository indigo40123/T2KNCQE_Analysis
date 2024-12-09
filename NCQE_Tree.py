import ROOT
from array import array

class NCQE__mc:

    def __init__(self, filename="ncqe_selected_mc.root", treename="NCQETree", title="selected T2K NCQE MC"):
        """
        Initializes the EventTreeWriter by creating a ROOT file and TTree, and defining branches.

        Parameters:
        - filename (str): Name of the output ROOT file.
        - treename (str): Name of the TTree.
        - title (str): Title of the TTree.
        """
        #Create the output ROOT file
        #self.file = ROOT.TFile(filename, "RECREATE")
        #if self.file.IsZombie():
        #    raise IOError(f"Could not create ROOT file: {filename}")
        
        # Create the TTree
        self.tree = ROOT.TTree(treename, title)

        # Initialize branch variables as arrays
        self.enu      = array('f', [0.0])  # nu energy [MeV]
        self.erec     = array('f', [0.0])  # visible energy [MeV]
        self.dwall    = array('f', [0.0])  # dwall [cm]
        self.effwall  = array('f', [0.0])  # effwall [cm]
        self.ovaq     = array('f', [0.0])  # ovaQ [arb]
        self.angle    = array('f', [0.0])  # Cherenkov angle [degree]
        self.pos_x    = array('f', [0.0])  # Bonsai Vertex X [m]
        self.pos_y    = array('f', [0.0])  # Bonsai Vertex Y [m]
        self.pos_z    = array('f', [0.0])  # Bonsai Vertex Z [m]
        self.pos_r2   = array('f', [0.0])  # Radius squared [m^2]
        self.posvx    = array('f', [0.0])  # MC truth Vertex X [m]
        self.posvy    = array('f', [0.0])  # MC truth Vertex Y [m]
        self.posvz    = array('f', [0.0])  # MC truth Vertex Z [m]
        self.bdir_x   = array('f', [0.0])  # Bonsai Direction X
        self.bdir_y   = array('f', [0.0])  # Bonsai Direction Y
        self.bdir_z   = array('f', [0.0])  # Bonsai Direction Z
        self.cosb     = array('f', [0.0])  # Cosine of angle
        self.Ntrue    = array('i', [0])     # MC truth Nmulti
        self.Ntaggable= array('i', [0])     # Pre-selection NMulti
        self.Ntagged  = array('i', [0])     # NN-selected Nmulti

        # Create branches in the TTree
        self.tree.Branch("enu", self.enu, "enu/F")
        self.tree.Branch("erec", self.erec, "erec/F")
        self.tree.Branch("dwall", self.dwall, "dwall/F")
        self.tree.Branch("effwall", self.effwall, "effwall/F")
        self.tree.Branch("ovaq", self.ovaq, "ovaq/F")
        self.tree.Branch("angle", self.angle, "angle/F")
        self.tree.Branch("pos_x", self.pos_x, "pos_x/F")
        self.tree.Branch("pos_y", self.pos_y, "pos_y/F")
        self.tree.Branch("pos_z", self.pos_z, "pos_z/F")
        self.tree.Branch("pos_r2", self.pos_r2, "pos_r2/F")
        self.tree.Branch("posvx", self.posvx, "posvx/F")
        self.tree.Branch("posvy", self.posvy, "posvy/F")
        self.tree.Branch("posvz", self.posvz, "posvz/F")
        self.tree.Branch("bdir_x", self.bdir_x, "bdir_x/F")
        self.tree.Branch("bdir_y", self.bdir_y, "bdir_y/F")
        self.tree.Branch("bdir_z", self.bdir_z, "bdir_z/F")
        self.tree.Branch("cosb", self.cosb, "cosb/F")
        self.tree.Branch("Ntrue", self.Ntrue, "Ntrue/I")
        self.tree.Branch("Ntaggable", self.Ntaggable, "Ntaggable/I")
        self.tree.Branch("Ntagged", self.Ntagged, "Ntagged/I")

    def fill(self, enu, erec, dwall, effwall, ovaq, angle,
             pos_x, pos_y, pos_z, pos_r2, posvx, posvy, posvz,
             bdir_x, bdir_y, bdir_z, cosb, Ntrue, Ntaggable, Ntagged):
        """
        Assigns values to the branches and fills the TTree.

        Parameters:
        - All parameters correspond to the branches defined during initialization.
        """
        # Assign values to the arrays
        self.enu[0]      = enu
        self.erec[0]     = erec
        self.dwall[0]    = dwall
        self.effwall[0]  = effwall
        self.ovaq[0]     = ovaq
        self.angle[0]    = angle

        self.pos_x[0]    = pos_x
        self.pos_y[0]    = pos_y
        self.pos_z[0]    = pos_z
        self.pos_r2[0]   = pos_r2
        self.posvx[0]    = posvx
        self.posvy[0]    = posvy
        self.posvz[0]    = posvz

        self.bdir_x[0]   = bdir_x
        self.bdir_y[0]   = bdir_y
        self.bdir_z[0]   = bdir_z
        self.cosb[0]     = cosb

        self.Ntrue[0]    = Ntrue
        self.Ntaggable[0] = Ntaggable
        self.Ntagged[0]  = Ntagged

        # Fill the tree with the current event's data
        self.tree.Fill()

