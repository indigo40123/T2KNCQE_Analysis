##############################################################  
The analysis code used for T2K NCQE Run 11 (SK-VI) analysis.      
Code itself was inherited from numerous predecessors.             
This version, reorganized with class, contains key parameters.  
##############################################################   
                                                               
The main analysis codes are main_SKDETSIM.py and main_SKG4.py.  
Usage: python main_SKDETSIM.py [inputfile]                        
       python main_SKG4.py [inputfile]                           

The Run 11 (SK-VI) MC file are provided in /MC_sample   
with different detector simulation settings    
/BERT_SKG4 , /INCL_SKG4 or /SKDETSIM_263   

The selection of the main analysis code depends on whether  
the input file is generated using SKDETSIM or SKG4, as these   
two frameworks have slightly different parameter naming conventions.  
An automatic checking mechanism could be considered for future improvements. 

############# Class are defined as follows ###################  

1. T2K_Config.py : Includes neutrino oscillation parameters,   
                   neutrino beam direction, proton-on-target (POT),  
                   flux tunning file, and NCQE cross-section.  

2. NCQE_Cut.py   : Includes the NCQE cuts parameters run-by-run and   
                   the channel definition is also given here.  
           
3. NCQE_Tree.py  : Includes the tree structure definition to save  
                   the selected NCQE event information.  

4. NCQE_Gamma_Hist.py : Includes the 1D histogram definition to save  
                        the selected NCQE gamma event features.  

5. NCQE_Neutron_Hist.py : Includes the 1D histogram definition to save  
                        the selected NCQE neutron event features.  
################################################################  

Last updated by LiCheng FENG on December 7, 2024.




