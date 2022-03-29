from pymol import cmd


#def loadpdbED(pdbf,resn,ED,DED):
def loadpdbED(pdbf, resn, ED, DED):
    cmd.reinitialize
    cmd.bg_color('1 1 1')
    cmd.set('orthoscopic','1')
    cmd.set('fog','1')

    cmd.load(pdbf)
    cmd.hide('everything','all')

    cmd.select("lig","resn "+resn)
    
    cmd.select("site","(byres (resn "+ resn + ")expand 4.0)")
    cmd.show_as("wire","site")
    
    cmd.show_as("licorice","lig")
    
    
    #cmd.label('''(name CA+C1*+C1' and (byres(site)))''','''"%s-%s"%(resn,resi)''')
    cmd.util.cbay("lig")

    cmd.load(ED,'2fcfo')
    cmd.isomesh('mapb', '2fcfo', level=1.0, selection='site', carve=2.0)
    cmd.color('blue','mapb')
    cmd.set('transparency','0.8','mapb')

    cmd.load(DED,'fcfo')
    cmd.isomesh('mapr', 'fcfo', level=-3.0, selection='site', carve=2.0)
    cmd.color('red','mapr')

    cmd.isomesh('mapg', 'fcfo', level=3.0, selection='site', carve=2.0)
    cmd.color('green','mapg')
#
    cmd.zoom("site",animate=-1)
    #
    #cmd.set_view((view))
#
    cmd.ray(600,600)
    cmd.png('pdbf'+'.png',1200,1200,300,1)

cmd.extend('loadpdbED', loadpdbED)