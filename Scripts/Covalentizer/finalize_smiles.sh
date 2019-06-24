grep '.' results.txt | awk '$NF < 1' | awk '{print $NF}' > rmsd.list
grep '.' results.txt | awk '$NF < 1' | awk -F '.' '{print $1}' > index.list
for i in `grep '.' results.txt | awk '$NF < 1' | awk -F '.' '{print $1}'` ; do grep SMILES poses.mol2 | awk '{print $NF}' | head -${i} | tail -1 ; done > smiles.list
for i in `grep '.' results.txt | awk '$NF < 1' | awk -F '.' '{print $1}'` ; do grep Name poses.mol2 | grep -v 'Long' | awk '{print $NF}' | head -${i} | tail -1 | awk -F '.' '{print $1}' ; done > names.list
paste smiles.list names.list rmsd.list index.list | sort -k3,3 -n | awk '!x[$1]++' | cat -n > data.txt
python /home/danielza/CovaLib/Scripts/ExtractPoses.py poses.mol2 index.list
for i in `wc -l data.txt | awk '$1 > 0' | awk '{print $1}'` ; do mkdir web_files/ ; done
cat data.txt | awk '{print "cp poses/"$5".mol2 web_files/"$1".mol2 ; echo \""$2"\" > web_files/"$1".smi ; echo "$4" > web_files/"$1".rmsd"}' > make_web_folder.sh ; chmod 777 make_web_folder.sh ; ./make_web_folder.sh
cp ../rec.pdb web_files/
cp ../xtal-lig.pdb web_files/
cat ../../../res.txt | awk '{print $2}' > web_files/cys_position.txt
cd web_files/
for i in *.smi ; do python /home/danielza/Work/Current/Covalentizer/scripts/reform_elec.py /home/danielza/Work/Current/Covalentizer/scripts/reform_elec.re $i tmp.smi ; cat tmp.smi | awk '{print $1}' > $i ; python /home/danielza/Work/Current/Covalentizer/scripts/draw_smile.py $i ; done ; rm tmp.smi
cd ../
