from pymol import cmd

#def loadpdbED(pdbf,resn,ED,DED):
def loadpdbED_DSN6(name, resn):
	
    cmd.reinitialize
    cmd.bg_color('1 1 1')
    cmd.set('orthoscopic','1')
    cmd.set('fog','1')

    cmd.load(name+'.pdb')
    cmd.hide('everything','all')
	
    cmd.select("lig","resn "+resn)
    
    cmd.select("site","(byres (resn "+ resn + ")expand 4.0)")
    cmd.show_as("stick","site")
    
    cmd.show_as("licorice","lig")
    
    
    #cmd.label('''(name CA+C1*+C1' and (byres(site)))''','''"%s-%s"%(resn,resi)''')
    cmd.util.cbay("lig")

    cmd.load(name+'_2fofc.dsn6','2fcfo')
    cmd.isomesh('mapb', '2fcfo', level=1.0, selection='site', carve=2.0)
    cmd.color('blue','mapb')
    cmd.set('transparency','0.8','mapb')

    cmd.load(name+'_fofc.dsn6','fcfo')
    cmd.isomesh('mapr', 'fcfo', level=-3.0, selection='site', carve=2.0)
    cmd.color('red','mapr')

    cmd.isomesh('mapg', 'fcfo', level=3.0, selection='site', carve=2.0)
    cmd.color('green','mapg')
#
    cmd.zoom("site",animate=-1)
	#view
    try:
        view=[0]*18
        fv=open('view.dat','r')
        fv.readline()
        for i in range(6):
            line=fv.readline()
            var=line.replace(")"," ").replace("\\"," ").split(",")
            view[i*3]=float(var[0])
            view[i*3+1]=float(var[1])
            view[i*3+2]=float(var[2])
        fv.close()
        cmd.set_view(view)
        cmd.ray(1200,1200)
        cmd.png(name+'.png',1200,1200,500,1)
    except IOError:
        print("view.dat is not accessible.")
    #
    #cmd.set_view((view))
#
    #cmd.ray(600,600)
    #cmd.png(name+'.png',1200,1200,300,1)

cmd.extend('loadpdbED_DSN6', loadpdbED_DSN6)