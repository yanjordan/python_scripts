from pymol import cmd

def str2cr(resstr): #input string to chain and residue num
    if resstr.isdigit():
        chain="A" # Chain A in default
        resi=resstr
    else:
        chain=resstr[0:1]
        resi=resstr[1:]
    return chain, resi 

def reslist(selection,output='N'):
	listres=""
	counter=0
	sel=selection
	objs=cmd.get_object_list(sel)
	
	for a in range(len(objs)):
		m1=cmd.get_model(sel+" and "+objs[a])
		for x in range(len(m1.atom)):
			if m1.atom[x-1].resi!=m1.atom[x].resi:
				listres+="%s %s%s " %(m1.atom[x].chain, m1.atom[x].resn, m1.atom[x].resi)
				counter+=1
				
	print("Residues in '%s': %s" %(selection, counter))
	
	if output=="S": 
		print(listres)
	if output=="P":
		print(listres)
		f=open('Listres_'+selection+'.txt','w')
		f.write("Residues in '%s': %s\n" % (selection, counter))
		f.write(listres)
		f.close()
		print("Results saved in Listres__%s.txt" %(selection))

def ShowOniom(resi, mrad='3.0',rrad='0.0',high='0.01'):
    #cmd.hide('everything','all')
    cmd.bg_color('1 1 1')
    cmd.set('orthoscopic','1')
    cmd.set('fog','1')
    
    #cmd.load(name+'.pdb')
    
    cmd.set('cartoon_oval_quality', '100')
    cmd.set('sphere_quality', '2')
    cmd.set('stick_quality', '30')
    cmd.set('surface_quality', '3')
    cmd.set('sphere_scale', '0.24')
    #cmd.set('sphere_mode', '4')

    cmd.hide('lines')
    cmd.hide('nonbonded')
    cmd.hide('spheres')
    cmd.hide('licorice')
    
    chain, resnum=str2cr(resi)
    
    cmd.select("centerres","resi "+resnum)
    
    cmd.select("highlayer","(byres centerres expand "+ high +")")
    cmd.select("mediumlayer","(byres centerres expand "+ mrad +" and (not highlayer))")
    cmd.select("relaxed","(byres centerres expand "+ rrad +")")
	
    reslist('highlayer','P')
    reslist('mediumlayer','P')
    
    cmd.set('stick_radius', '0.2')
    cmd.show('sticks','relaxed')
    #mediwum layer
    cmd.show("sticks","mediumlayer")
    cmd.set('line_width','1')
    cmd.util.cba('154',"mediumlayer")
    #highlayer
    cmd.set('stick_radius', '0.15',"highlayer")
    cmd.set('sphere_scale', '0.25',"highlayer")
    
    cmd.show("licorice","highlayer")
    cmd.show("spheres","highlayer")
    
    cmd.util.cba('6',"relaxed")
    
    cmd.zoom("mediumlayer",animate=-1)
    
cmd.extend('ShowOniom', ShowOniom)
#ShowOniom('5p9i_a_flip_ligH', '701')
