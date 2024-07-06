# import re
# text="""So, the reactions are scored as:
# Reaction 1 : 0.38166692
# Reaction 2 : 0.21646441
# Reaction 3 : 0.29255616
# Reaction 4 : 0.28464431
# Reaction 5 : 0.18633515
# Reaction 6 : 0.21646441
# """

# # 使用正则表达式提取分数
# scores = re.findall(r'Reaction \d+ : ([\d.]+)', text)

# # 将分数转换为浮点数
# scores = [float(score) for score in scores]

# print(scores)
import os 
from rdkit import Chem
from rdkit.Chem import ChemicalFeatures
from rdkit import RDConfig
from rdkit.Chem import Draw
fdefName = os.path.join(RDConfig.RDDataDir,'BaseFeatures.fdef')
factory = ChemicalFeatures.BuildFeatureFactory(fdefName)

smi='C=CC(=O)N1CCC(CC1)C2CCNC3=C(C(=NN23)C4=CC=C(C=C4)OC5=CC=CC=C5)C(=O)N'
m=Chem.MolFromSmiles(smi)
feats = factory.GetFeaturesForMol(m)
len(feats)
for f in feats:
    print(f.GetFamily(),f.GetType(),f.GetAtomIds())
fName=os.path.join(RDConfig.RDDataDir,'FunctionalGroups.txt')
from rdkit.Chem import FragmentCatalog
fparams = FragmentCatalog.FragCatParams(1,6,fName)
fparams.GetNumFuncGroups()
mols=[]
for i in range(fparams.GetNumFuncGroups()):
    mols.append(fparams.GetFuncGroup(i))
print(mols[0].smiles())
Draw.MolsToGridImage(mols,molsPerRow=8)