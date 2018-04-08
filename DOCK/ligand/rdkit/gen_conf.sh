echo -------------
date
mkdir tmp
cd tmp
echo 'gen conf' "$1"
python $DOCKBASE/ligand/rdkit/RDkit_GenConf.py ../"$1" 250
date
echo  'adding charge'
$OBABELBASE/obabel -ipdb rdkit_conf.pdb -omol2 -r -m -Oconf.mol2 

for d in conf*.mol2
do
 python $DOCKBASE/ligand/rdkit/addCharge2mol2.py "$d" ../"$1"
done
echo 'translate to mol2 conf'
$OBABELBASE/obabel -imol2 c_conf*.mol2 -omol2 --readconformers -Ordkit_conf.db2in.mol2
cp rdkit_conf.db2in.mol2 ../output.1.db2in.mol2
cd ..
#rm -r tmp
date
echo -------------
