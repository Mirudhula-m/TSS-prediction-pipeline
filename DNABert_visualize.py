import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import pandas as pd
import shutil
import os


# Initialize the argument parser
parser = argparse.ArgumentParser(description='Process input file')
parser.add_argument('-n', '--data_name', type=str, required=True, help='Name of cage directory that was used initially')
parser.add_argument('-user', '--user_name', type=str, required=True, help='User name on bridges2')

# Parse the arguments
args = parser.parse_args()

DEEPTSS_DIR="/ocean/projects/bio230007p/"+args.user_name+"/DeepTSS/data/"+args.data_name+"/OUT"
# High confidence
dt_path_high = DEEPTSS_DIR+"/high_prob/dev.tsv"
# Low confidence
dt_path_low = DEEPTSS_DIR+"/low_prob/dev.tsv"


with open(dt_path_high, 'r') as file:
    # Use the NumPy genfromtxt function to load the TSV file
    data = np.genfromtxt(file, delimiter='\t')
    # Extract the second column -- labels
    deeptss_pred_high = data[1:, 1].astype(int)
with open(dt_path_low, 'r') as file:
    # Use the NumPy genfromtxt function to load the TSV file
    data = np.genfromtxt(file, delimiter='\t')
    # Extract the second column -- labels
    deeptss_pred_low = data[1:, 1].astype(int)




DNABERT_PATH="/ocean/projects/bio230007p/"+args.user_name+"/DNABert"
OUT_PATH="/ocean/projects/bio230007p/"+args.user_name+"/DNABert/OUT/"+args.data_name
if not os.path.exists(OUT_PATH):

    os.makedirs(OUT_PATH)
    os.makedirs(OUT_PATH+"/high")
    os.makedirs(OUT_PATH+"/low")

high_path = OUT_PATH+"/high"
low_path = OUT_PATH+"/low"

high_tmp_path = DNABERT_PATH+"/OUT/high"
# get a list of all the files in the source folder
high_files = os.listdir(high_tmp_path)
# iterate over each file and copy it to the destination folder
for file_name in high_files:
    src_file = os.path.join(high_tmp_path, file_name)
    shutil.copy(src_file, high_path)

low_tmp_path = DNABERT_PATH+"/OUT/low"
low_files = os.listdir(low_tmp_path)
for file_name in low_files:
    src_file = os.path.join(low_tmp_path, file_name)
    shutil.copy(src_file, low_path)


# Load the prediction results and attention weights
pred_results_high = np.load(high_path+'/preds.npy')
pred_results_low = np.load(low_path+'/preds.npy')

atten_high = np.load(high_path+'/atten.npy')
atten_low = np.load(low_path+'/atten.npy')

print(deeptss_pred_high.shape, pred_results_high.shape)
print(deeptss_pred_low.shape, pred_results_low.shape)
print(atten_high.shape)
print(deeptss_pred_high[0])
print(pred_results_high[0])

# Visualize the prediction results
# Create confusion matrix
confusion_matrix = np.zeros((2,2))
for i in range(len(deeptss_pred_high)):
    confusion_matrix[deeptss_pred_high[i], pred_results_high[i]] += 1

# Plot confusion matrix using Seaborn
plt.figure()
sns.set()
sns.heatmap(confusion_matrix, annot=True, cmap='Blues')
plt.xlabel('DNABert Predictions')
plt.ylabel('DeepTSS Predictions')
plt.savefig(high_path+'/confusion.png')

confusion_matrix = np.zeros((2,2))
for i in range(len(deeptss_pred_low)):
    confusion_matrix[deeptss_pred_low[i], pred_results_low[i]] += 1

# Plot confusion matrix using Seaborn
plt.figure()
sns.set()
sns.heatmap(confusion_matrix, annot=True, cmap='Blues')
plt.xlabel('DNABert Predictions')
plt.ylabel('DeepTSS Predictions')
plt.savefig(low_path+'/confusion.png')





# Calculate metrics using scikit-learn

accuracy = accuracy_score(deeptss_pred_high, pred_results_high)
recall = recall_score(deeptss_pred_high, pred_results_high)
precision = precision_score(deeptss_pred_high, pred_results_high)
f1 = f1_score(deeptss_pred_high, pred_results_high)

# Create a dictionary to store the metrics
metrics_dict = {'Accuracy': accuracy, 'Recall': recall, 'Precision': precision, 'F1 Score': f1}

# Convert the dictionary to a pandas DataFrame
metrics_df = pd.DataFrame(metrics_dict, index=[0])

# Melt the DataFrame to long format
metrics_long = pd.melt(metrics_df, var_name='Metric', value_name='Score')

# Plot the bar plot using Seaborn
plt.figure()
sns.set_style('whitegrid')
sns.barplot(x='Metric', y='Score', data=metrics_long, palette='Blues_d')
plt.title('Metrics Summary')
plt.ylim(0, 1)
plt.savefig(high_path+'/bar.png')

# Calculate metrics using scikit-learn
accuracy = accuracy_score(deeptss_pred_low, pred_results_low)
recall = recall_score(deeptss_pred_low, pred_results_low)
precision = precision_score(deeptss_pred_low, pred_results_low)
f1 = f1_score(deeptss_pred_low, pred_results_low)

# Create a dictionary to store the metrics
metrics_dict = {'Accuracy': accuracy, 'Recall': recall, 'Precision': precision, 'F1 Score': f1}

# Convert the dictionary to a pandas DataFrame
metrics_df = pd.DataFrame(metrics_dict, index=[0])

# Melt the DataFrame to long format
metrics_long = pd.melt(metrics_df, var_name='Metric', value_name='Score')

# Plot the bar plot using Seaborn
plt.figure()
sns.set_style('whitegrid')
sns.barplot(x='Metric', y='Score', data=metrics_long, palette='Blues_d')
plt.title('Metrics Summary')
plt.ylim(0, 1)
plt.savefig(low_path+'/bar.png')






ave = np.sum(atten_high)/atten_high.shape[1]
# Visualize the attention weights
plt.figure()
sns.set()
ax = sns.heatmap(atten_high, cmap='YlGnBu', vmin=0)
plt.xlabel('Input sequence position')
plt.ylabel('Output sequence position')
plt.title('Attention weights')
plt.savefig(high_path+'/attention_weights.png')


ave = np.sum(atten_low)/atten_low.shape[1]
# Visualize the attention weights
plt.figure()
sns.set()
ax = sns.heatmap(atten_low, cmap='YlGnBu', vmin=0)
plt.xlabel('Input sequence position')
plt.ylabel('Output sequence position')
plt.title('Attention weights')
plt.savefig(low_path+'/attention_weights.png')



