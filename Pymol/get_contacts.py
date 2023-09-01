#!/usr/bin/python

'''PyMOL plugin that provides show_contacts command and GUI 
for highlighting good and bad polar contacts. Factored out of 
clustermols by Matthew Baumgartner.
The advantage of this package is it requires many fewer dependencies.
'''
from __future__ import print_function

import sys,os
from pymol import cmd

DEBUG=1

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


def get_contacts(resi,result="contacts",cutoff=3.6, bigcutoff = 4.0, SC_DEBUG = DEBUG):
    """
    USAGE
    
    show_contacts selection, selection2, [result=contacts],[cutoff=3.6],[bigcutoff=4.0]
    
    Show various polar contacts, the good, the bad, and the ugly.
    
    Edit MPB 6-26-14: The distances are heavy atom distances, so I upped the default cutoff to 4.0
    
    Returns:
    True/False -  if False, something went wrong
    """
    cchain, resnum=str2cr(resi)

    cmd.select("centerres","resi "+resnum)
    cmd.select("buffer","(byres centerres expand 4.0 and (not centerres))")

    #print list res
    reslist('centerres','S')
    reslist('buffer','S')

    result = cmd.get_legal_name(result)

    #if the group of contacts already exist, delete them
    cmd.delete(result)

    # ensure only N and O atoms are in the selection
    all_don_acc1 = "centerres and (donor or acceptor)"
    all_don_acc2 = "buffer and  (donor or acceptor)"
    
        
    #if theses selections turn out not to have any atoms in them, pymol throws cryptic errors when calling the dist function like:
    #'Selector-Error: Invalid selection name'
    #So for each one, manually perform the selection and then pass the reference to the distance command and at the end, clean up the selections
    #the return values are the count of the number of atoms
    all1_sele_count = cmd.select('all_don_acc1_sele', all_don_acc1)
    all2_sele_count = cmd.select('all_don_acc2_sele', all_don_acc2)
    
    #print out some warnings
    if DEBUG > 3:
        if not all1_sele_count:
            print('Warning: all_don_acc1 selection empty!')
        if not all2_sele_count:
            print('Warning: all_don_acc2 selection empty!')
    
    ########################################
    allres = result + "_all"
    if all1_sele_count and all2_sele_count:
        cmd.distance(allres, 'all_don_acc1_sele', 'all_don_acc2_sele', bigcutoff, mode = 0)
        cmd.set("dash_radius", "0.05", allres)
        cmd.set("dash_color", "purple", allres)
        cmd.hide("labels", allres)
    
    ########################################
    #compute good polar interactions according to pymol
    polres = result + "_polar"
    if all1_sele_count and all2_sele_count:
        cmd.distance(polres, 'all_don_acc1_sele', 'all_don_acc2_sele', cutoff, mode = 2) #hopefully this checks angles? Yes
        cmd.set("dash_radius","0.126",polres)
    
    ########################################
    #When running distance in mode=2, the cutoff parameter is ignored if set higher then the default of 3.6
    #so set it to the passed in cutoff and change it back when you are done.
    old_h_bond_cutoff_center = cmd.get('h_bond_cutoff_center') # ideal geometry
    old_h_bond_cutoff_edge = cmd.get('h_bond_cutoff_edge') # minimally acceptable geometry
    cmd.set('h_bond_cutoff_center', bigcutoff)
    cmd.set('h_bond_cutoff_edge', bigcutoff)
        
    #compute possibly suboptimal polar interactions using the user specified distance
    pol_ok_res = result + "_polar_ok"
    if all1_sele_count and all2_sele_count:
        cmd.distance(pol_ok_res, 'all_don_acc1_sele', 'all_don_acc2_sele', bigcutoff, mode = 2) 
        cmd.set("dash_radius", "0.06", pol_ok_res)

    #now reset the h_bond cutoffs
    cmd.set('h_bond_cutoff_center', old_h_bond_cutoff_center)
    cmd.set('h_bond_cutoff_edge', old_h_bond_cutoff_edge) 
    
    
    ########################################
    
    onlyacceptors1 = "centerres and (acceptor and !donor)"
    onlyacceptors2 = "buffer and (acceptor and !donor)"
    onlydonors1 = "centerres and (!acceptor and donor)"
    onlydonors2 = "buffer and (!acceptor and donor)"  
    
    #perform the selections
    onlyacceptors1_sele_count = cmd.select('onlyacceptors1_sele', onlyacceptors1)
    onlyacceptors2_sele_count = cmd.select('onlyacceptors2_sele', onlyacceptors2)
    onlydonors1_sele_count = cmd.select('onlydonors1_sele', onlydonors1)
    onlydonors2_sele_count = cmd.select('onlydonors2_sele', onlydonors2)    
    
    #print out some warnings
    if SC_DEBUG > 2:
        if not onlyacceptors1_sele_count:
            print('Warning: onlyacceptors1 selection empty!')
        if not onlyacceptors2_sele_count:
            print('Warning: onlyacceptors2 selection empty!')
        if not onlydonors1_sele_count:
            print('Warning: onlydonors1 selection empty!')
        if not onlydonors2_sele_count:
            print('Warning: onlydonors2 selection empty!')    
            
    
    accres = result+"_aa"
    if onlyacceptors1_sele_count and onlyacceptors2_sele_count:
        aa_dist_out = cmd.distance(accres, 'onlyacceptors1_sele', 'onlyacceptors2_sele', cutoff, 0)

        if aa_dist_out < 0:
            print('\n\nCaught a pymol selection error in acceptor-acceptor selection of show_contacts')
            print('accres:', accres)
            print('onlyacceptors1', onlyacceptors1)
            print('onlyacceptors2', onlyacceptors2)
            return False
    
        cmd.set("dash_color","red",accres)
        cmd.set("dash_radius","0.125",accres)
    
    ########################################
    
    donres = result+"_dd"
    if onlydonors1_sele_count and onlydonors2_sele_count:
        dd_dist_out = cmd.distance(donres, 'onlydonors1_sele', 'onlydonors2_sele', cutoff, 0)
        
        #try to catch the error state 
        if dd_dist_out < 0:
            print('\n\nCaught a pymol selection error in dd selection of show_contacts')
            print('donres:', donres)
            print('onlydonors1', onlydonors1)
            print('onlydonors2', onlydonors2)
            print("cmd.distance('" + donres + "', '" + onlydonors1 + "', '" + onlydonors2 + "', " + str(cutoff) + ", 0)")  
            return False
        
        cmd.set("dash_color","red",donres)  
        cmd.set("dash_radius","0.125",donres)
    
    ##########################################################
    ##### find the buried unpaired atoms of the receptor #####
    ##########################################################
    
    #initialize the variable for when CALC_SASA is False
    unpaired_atoms = ''
    
        
    ## Group
    cmd.group(result,"%s %s %s %s %s %s" % (polres, allres, accres, donres, pol_ok_res, unpaired_atoms))
    
    ## Clean up the selection objects
    #if the show_contacts debug level is high enough, don't delete them.
    if SC_DEBUG < 5:
        cmd.delete('all_don_acc1_sele')
        cmd.delete('all_don_acc2_sele')
        cmd.delete('onlyacceptors1_sele')
        cmd.delete('onlyacceptors2_sele')
        cmd.delete('onlydonors1_sele')
        cmd.delete('onlydonors2_sele')
    
    
    return True
cmd.extend('get_contacts', get_contacts) #contacts to avoid clashing with cluster_mols version



    