from pymol import cmd
import os


def VIZ_frag_savepng(name='XX'):
    #view
    try:
        view=[0]*18
        fv=open('frag_view.dat','r')
        fv.readline()
        for i in range(6):
            line=fv.readline()
            var=line.replace(")"," ").replace("\\"," ").split(",")
            view[i*3]=float(var[0])
            view[i*3+1]=float(var[1])
            view[i*3+2]=float(var[2])
        fv.close()
        cmd.set_view(view)
    except IOError:
        print("frag_view.dat is not accessible.")
	
    cmd.ray(1200,1200)
	
    cmd.png(name+'.png',1200,1200,600,1)

cmd.extend('VIZ_frag_savepng', VIZ_frag_savepng)