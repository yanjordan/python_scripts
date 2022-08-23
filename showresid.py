from pymol import cmd


def showresid(resnum,chain='A',rad='4.0'):
<<<<<<< HEAD
    cmd.hide('everything','all')
    cmd.select("centerres","resi "+resnum+" and (chain "+chain+")")
    
    cmd.select("ressite","(byres centerres expand "+ rad +")")
=======
#def showresid(resnum,rad='4.0'):
    cmd.hide('everything','all')
    #cmd.select("centerres","resi "+resnum)
    cmd.select("centerres","chain "+chain+" and (resi "+resnum+")")
    
    cmd.select("ressite","(byres centerres expand "+ rad +")")
    #cmd.select("ressite","(byres (chain " + chain + "and (resi "+ resnum + ")) expand "+ rad +")")
>>>>>>> 75766d8177fb5f1838eef933d7fb687d1a7239a6
    cmd.show_as("wire","ressite")
    
    cmd.show_as("licorice","centerres")
    
    cmd.zoom("ressite",animate=-1)
    cmd.label('''(name CA+C1*+C1' and (byres(ressite)))''','''"%s-%s"%(resn,resi)''')
    

cmd.extend('showresid', showresid)

