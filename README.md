# Pymol_scripts
some extended functions of pymol

## installation
Pymol --> Plugin --> Plugin Manager --> Install New Plugin --> Choose file... --> path of script

## scripts
### showresid.py
usage： showresid chain+resid
        showresid chain+resid, dis  
        chain is optional, default chain A without chain info
show residue (id number) with licorice, and this neighbouring (< 4 (dis) angstrom>) residues with wire


### loadpdbgED.py
loadpdbgED PDB(remove .pdb), resn
show electron density (sigma, blue) and difference of electon densiy (+ & - 3 sigma, red and green) around residue (resn) with licorice, and this neighbouring (< 4 angstrom>) residues with wire

### savepng.py
savepng name
save as name.png if no name give then save XX.png