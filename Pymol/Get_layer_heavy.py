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
	num_atom = cmd.count_atoms(sel)			
	print("Residues in '%s': %s" %(selection, counter))
	print("Atoms in '%s': %s" %(selection, num_atom))
	
	

	if output=="S": 
		print(listres)
	if output=="P":
		print(listres)
		f=open('Listres_'+selection+'.txt','w')
		f.write("Residues in '%s': %s\n" % (selection, counter))
		f.write(listres)
		f.close()
		print("Results saved in Listres__%s.txt" %(selection))

def chain_resi(reslist):
	chains = []
	resis = []
	for resstr in reslist:
		chain, resi=str2cr(resstr)
		if chain not in chains:
			chains.append(chain)
			resis.append(resi)
		else:
			index = chains.index(chain)
			resis[index] += "+" + resi
			
	if len(chains)==1:
		chain_resi_str = "Chain "+chains[0]+" and resi "+resis[0]
	else:
		chain_resi_str = "("
		for i in range(len(chains)):
			chain_resi_str += "Chain "+chains[i]+" and resi "+resis[i]
			if i != len(chains)-1:
				chain_resi_str += ") or ("
			else:
				chain_resi_str += ")"
	return chain_resi_str

def get_pdb_info(pdb_file, res, rad='3.0'):
    cmd.reinitialize()
    # 加载PDB文件
    pdbname = pdb_file.split(".")[0]

    cmd.load(pdb_file)
    cmd.copy(pdbname+'_noH',pdbname)
    cmd.remove(pdbname+'_noH and elem H')

    chain, resnum=str2cr(res)
    #选取 pdbname 的指定残基及其周围3A 范围内残基
    #cmd.select('centerres',pdbname+" and resi "+resnum+" and (chain "+chain+")")
    #cmd.select("highsite",pdbname+" and (byres centerres expand "+ rad +")")

    cmd.select('centerres_noH',pdbname+"_noH and resi "+resnum)
    cmd.select("highsite_noH",pdbname+"_noH and (byres centerres_noH expand "+ rad +")")
    
    mysapce = {'ress': [], 'IDs':[]}
    cmd.iterate("highsite_noH", 'ress.append(chain+resi)', space=mysapce)
    res_list = list(set(mysapce['ress']))
    chain_resistr = chain_resi(res_list)
    cmd.select("highsite_final",pdbname+" and "+chain_resistr)
    #cmd.select("highsite_final",pdbname+" and "+chain_resistr)
    #cmd.iterate("highsite_final", 'IDs.append(rank)', space=mysapce)
    #ID_list = list(set(mysapce['IDs']))
    num_atom = cmd.count_atoms("highsite_final")	
    print("There %s residues and % atoms in '%s" %(len(res_list), num_atom, 'highsite_final.xyz'))
    cmd.save('highsite_final.pdb','highsite_final')
    cmd.save('highsite_final.xyz','highsite_final')
    
cmd.extend('Get_layer_heavy', get_pdb_info)

