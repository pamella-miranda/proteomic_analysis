# -------------------------------------------------------
#   Last modified: 3 June 2025
#   
#   Venn diagram
#
#   file_path --> local for the output file
#   ext --> extension of the plots, e.g. eps, jpg, tif
#
#   python3.* venn_diagram.py file_path ext
#
#-------------------------------------------------------- 
import sys
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

file_path = sys.argv[1]
ext = sys.argv[2]

#Venn diagram
venn3(subsets = (75, 67, 8, 67, 8, 16, 9), 
      set_labels = ('red', 'green', 'blue'))

plt.savefig(file_path+"colours"+"."+ext,dpi=350)
plt.close()
