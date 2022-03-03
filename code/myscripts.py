import numpy as np
import pandas as pd
import os
import SimpleITK as sitk

from tensorflow.math import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay, f1_score, precision_score, accuracy_score, recall_score

# removal of scans 
def scan_removal(group, scan_type):
    """
    This function specifies a group of patients and scan type and removes the files in each directory as well the directory itself for that group and scan type

    Parameters
    ----------
    group: str 'control' or 'schiz'
    
    scan_type: str in scan type e.g. 'GATE', 'RST' or 'dti'
    """
    # specifying group
    if group == 'schiz':
        group = 'schizophrenic'
    elif group == 'control':
        group = 'no_known_disorder'
        
    # creating empty list to store all image paths
    scan_path_list = []
    
    # defining initial directory path by group
    group_dir = '../brain_images/'+group+'/cobre_07325/'
    
    # specifiying patients within directory
    patients = [each for each in os.listdir(group_dir)]
    for patient in patients:
        
        # specifying patient within group
        for session in os.listdir(group_dir+patient):
            
            # specifying session for patient
            for scan in os.listdir(group_dir+patient+'/'+session):
                
                # specifying and deleting files within scan directory
                if scan_type in scan:
                    image_dir = group_dir+patient+'/'+session+'/'+scan+'/'
                    scan_path_list.append(image_dir)
                    for each in os.listdir(image_dir):
                        # print(image_c_dir+each)
                        os.remove(image_dir+each)
                        
    # removing directory for scan                    
    for each in scan_path_list:
        os.removedirs(each)
    return (f'Succesfully removed {len(scan_path_list)} {group} {scan_type} directories')

# creating a list of dictionaries function
def array_dict(group, scan_type, patient_number, file_type):
    """
    This function creates a list of dictionaries specifying the path and numpy array for its image.

    Parameters
    ----------
    group: str 'control' or 'schiz'
    
    scan_type: str in scan type e.g. 't2', 'mprage' or 'dti'
    
    patient_number: str 'all' or string of number of patients
    
    file_type: str 'dcm' or 'nii'
    """
    
    # specifying group
    if group == 'schiz':
        group = 'schizophrenic'
    elif group == 'control':
        group = 'no_known_disorder'
    
    # path to directory per group
    group_dir = '../brain_images/'+group+'/cobre_07325/'
    arrays_dict = []
    
    # specifying which patients in group
    patients = [each for each in os.listdir(group_dir)]
    if patient_number == 'all':
        pass
    else:
        patients = patients[:int(patient_number)]
    
    # series of loops until in specified folder
    for patient in patients:
        for session in os.listdir(group_dir+patient):
            for scan in os.listdir(group_dir+patient+'/'+session):
                
                # specifies type of scan via a string
                if scan_type in scan:
                    image_dir = group_dir+patient+'/'+session+'/'+scan+'/'
                    for each in os.listdir(image_dir):
                        
                        # specifying a type of file via a string
                        if file_type in each:
                            try:
                                # reads in dcm files
                                image = sitk.ReadImage(image_dir+each)
                                
                                # change image into array & normalizes
                                image_arr = sitk.GetArrayFromImage(image)/255
                                
                                # appends a dictionary containing array and path
                                arrays_dict.append({'path': str(image_dir+each), 'scan': image_arr})
                            except:
                                print(f'Error for file: {each}')
    print(f'{len(arrays_dict)} pictures converted.')
    return arrays_dict

# creating metrics dataframe
def get_metrics_df(y_preds, y_test):
    # creating confusion matrix to derive specificity
    matrix = confusion_matrix(labels=y_test, predictions=y_preds, num_classes=2)

    # setting true negative and false positive
    tn, fp = matrix[0]

    # setting false negative and true positive
    fn, tp = matrix[1]

    # specificity
    spec = tn / (tn + fp)
    
    # dictionary of metrics
    dict_metrics = {'accuracy' : np.round(accuracy_score(y_test, y_preds), decimals=4),
                    'recall': np.round(recall_score(y_test, y_preds), decimals=4),
                    'precision': np.round(precision_score(y_test, y_preds), decimals=4),
                    'specificity': np.round(spec, decimals=4),
                    'f1 score': np.round(f1_score(y_test, y_preds), decimals=4),
                    'misclassification' : np.round(1-accuracy_score(y_test, y_preds), decimals=4)
           }
    
    # dataframe of metrics
    df = pd.DataFrame.from_dict(dict_metrics, orient='index')
    df = df.rename(columns={0:'scores'})
    return df

def find_combined_img(matrix, title, calculation, size = (192, 192), cmap='Greys_r'):
    # calculate the average
    if calculation == 'mean':
        comb_img = np.mean(matrix, axis = 0)
    if calculation == 'var':
        comb_img = np.var(matrix, axis = 0)
    if calculation == 'std':
        comb_img = np.std(matrix, axis = 0)
    # reshape it back to a matrix
    comb_img = comb_img.reshape(size)
    plt.imshow(comb_img, vmin=0, vmax=255, cmap=cmap)
    plt.title(f'Combined {title} by {calculation}')
    plt.axis('off')
    plt.show()
    return comb_img

# credit goes to this blog for the idea and general underpinning of code h/t classmate for suggestion
# https://towardsdatascience.com/exploratory-data-analysis-ideas-for-image-classification-d3fc6bbfb2d2