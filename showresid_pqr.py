from pymol import cmd

#def str2cr(resstr): #input string to chain and residue num
#    if resstr.isdigit():
#        chain="A" # Chain A in default
#        resi=resstr
#    else:
#        chain=resstr[0:1]
#        resi=resstr[1:]
#    return chain, resi 
    
def showresid_pqr(resi, rad='4.0'):
    cmd.hide('everything','all')
    
    cmd.select("centerres","resi "+resi)
    
    cmd.select("ressite","(byres centerres expand "+ rad +")")
    cmd.show_as("wire","ressite")
    
    cmd.show_as("licorice","centerres")
    
    cmd.zoom("ressite",animate=-1)
    cmd.label('''(name CA+C1*+C1' and (byres(ressite)))''','''"%s-%s"%(resn,resi)''')
    

cmd.extend('showresid_pqr', showresid_pqr)

