from pymol import cmd
import os

#def loadpdbED(pdbf,resn,ED,DED):
def savepng(name='XX'):

    cmd.ray(1200,1200)
	
    cmd.png(name+'.png',1200,1200,600,1)

cmd.extend('savepng', savepng)