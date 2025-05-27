# -----------------------------------------------------------------------------------------
#   Last modified: 22 January 2025
#
#   Principal Component Analysis (PCA) plot
#
#   dataset --> file.xlsx
#   sheet --> sheet of interest (samples in rows & genes/variables in columns)
#   samples --> initial and final (+1) numbers for sample codes
#   ext --> extension of the plots, e.g. eps, jpg, tif
#   file_path --> local for the output file
#   file_name --> name of the output file
#   code_plot --> code for the plot names
#
#   python3.* pca_plot.py file.xlsx sheet samples#1 samples#2 ext file_path file_name 
#   code_plot
#
# -----------------------------------------------------------------------------------------

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

dataset = sys.argv[1] #dataset
sheet = int(sys.argv[2]) #sheet of interest (samples in rows & genes/variables in columns)
samples = list(range(int(sys.argv[3]), int(sys.argv[4]))) #sample codes
ext = sys.argv[5] #extension of the figure
file_path = sys.argv[6] #path for output file --> e.g. ../file_path/
file_name = sys.argv[7] #output file --> e.g. output_file.xlsx
code_plot = sys.argv[8] #code for the plot names

#preparing the dataset
#samples in rows & genes/variables in columns
dataset = pd.read_excel(dataset, sheet_name=sheet)
samples_codes = dataset.drop(dataset.columns[1:],axis=1)
data_stats = dataset.drop(dataset.columns[0],axis=1)
genes_names = dataset.columns[1:]

#PCA on the dataset
#centering and scaling the data
std_scaler = StandardScaler()
scaled_data = std_scaler.fit_transform(data_stats)

#fitting the components
pca = PCA() #alternatively: pca = PCA(n_components=6)
pca_fit = pca.fit_transform(scaled_data)

#explained variance
#principal components (pc)
principal_component_list = [f'PC{i}' for i in list(range(1,len(pca_fit)+1))]
pca_explained_variance = ((pca.explained_variance_ratio_)*100)
explained_variance = pd.DataFrame(pca_explained_variance)
explained_variance.index = principal_component_list

plt.figure(figsize = (8,6))
plt.bar(principal_component_list,pca_explained_variance,color='purple', width=0.5)
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance (%)')
plt.title('Variance (%)')
plt.savefig(file_path+"pca_explained_variance_"+code_plot+"."+ext,dpi=350)
plt.close()

#pca scores
pca_scores = pd.DataFrame(data=pca_fit, columns=principal_component_list)

x = pca_scores['PC1']
y = pca_scores['PC2']
z = pca_scores['PC3']

colours_points = ['r','r','r','g','g','g']

fig,ax = plt.subplots()
plt.scatter(x, y, c=colours_points,s=100)

labels_points = []

for s in samples:
    code_sample = 'S'+str(s)
    labels_points.append(code_sample)

for i, label in enumerate(labels_points):
    ax.text(x[i], y[i], label)

pc1 = str(round(pca_explained_variance[0],1))
pc2 = str(round(pca_explained_variance[1],1))
pc3 = str(round(pca_explained_variance[2],1))

plt.xlabel("PC1 ("+pc1+"%)")
plt.ylabel("PC2 ("+pc2+"%)")
plt.title('Scores - PC1 x PC2')
plt.savefig(file_path+"pca_scores_2d_"+code_plot+"."+ext,dpi=350)
plt.close()

#pca in 3d
total_variance = str(round(pca_explained_variance[0] + pca_explained_variance[1] + pca_explained_variance[2], 1))

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(x, y, z, c=colours_points)

for i, label in enumerate(labels_points):
    ax.text(x[i], y[i], z[i], label)

ax.set_title('Total Explained Variance: '+total_variance+'%')
ax.set_xlabel('PC1 ('+pc1+'%)')
ax.set_ylabel('PC2 ('+pc2+'%)')
ax.set_zlabel('PC3 ('+pc3+'%)')

plt.savefig(file_path+"pca_scores_3d_"+code_plot+"."+ext,dpi=350)
plt.close()

#pca loadings
pca_loadings = (pca.components_).T
loadings = pd.DataFrame(data=pca_loadings,columns=principal_component_list)

colours_loadings = np.random.rand(len(loadings['PC1']))

plt.scatter(loadings['PC1'],loadings['PC2'],c=colours_loadings)

plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Loadings - PC1 x PC2')
plt.savefig(file_path+"pca_loadings_"+code_plot+"."+ext,dpi=350)
plt.close()

#pc1 contribution
pc1_genes = pd.Series(pca.components_[0],index=genes_names)
pc1_data = pc1_genes.abs().sort_values(ascending=False)
genes = pc1_data[:].index
ranked = pc1_data[:].values

#all data in a file
variance = pd.DataFrame(pca_explained_variance)
genes_names = pd.DataFrame(genes_names)
genes = pd.DataFrame(genes)
ranked = pd.DataFrame(ranked)

pca_data = pd.concat([variance,samples_codes,pca_scores,genes_names,loadings,genes,ranked], axis=1)
pca_data.columns = ['Explained Variance','Samples','PC1 - scores', 'PC2 - scores', 
                    'PC3 - scores', 'PC4 - scores', 'PC5 - scores', 'PC6 - scores', 
                    'Genes', 'PC1 - loadings', 'PC2 - loadings', 'PC3 - loadings', 
                    'PC4 - loadings', 'PC5 - loadings', 'PC6 - loadings','Genes',
                    'PC1 Contribution']

with pd.ExcelWriter(file_path+file_name) as writer:
    pca_data.to_excel(writer,sheet_name='pca data',index=False)
    
