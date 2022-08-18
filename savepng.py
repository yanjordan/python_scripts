from pymol import cmd
import os

#def loadpdbED(pdbf,resn,ED,DED):
def savepng(name='XX'):

    cmd.ray(600,600)
    cmd.png(name+'.png',1200,1200,300,1)

cmd.extend('savepng', savepng)