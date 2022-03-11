# Classification of Schizophrenia using CNNs with sMRIs 

## Problem Statement
Given structural MRI (T1 & T2) scans, can I build a model using CNNs to classify schizophrenic and non-schizophrenic brains? Are there differences between slice specific(horizontal/tranverse plane and verticel/sagittal plane) trained models?

## Background
Schizophrenia is a spectrum under psychotic disorders characterized by disturbances or dysfunctions in thinking(cognition), emotional responsiveness, andc behavior. The criterion for diagnosis require the persistence of at least 2 symptoms (delusions, hallucinations, disorganized speech, grossly disorganized or catatonic behavior, or negatives) for at least 1 month [(Source)](https://pro.psycom.net/assessment-diagnosis-adherence/schizophrenia#:~:text=disparities%20in%20schizophrenia.-,Schizophrenia%20Diagnosis,and%20Other%20Psychotic%20Disorders%20Class.). About 24 million people or 1 in 300 people worldwide have schizophrenia; 1 in 222 people among adults. Around 50% of people in mental hospitals have the diagnosis however only 31.3% of documented cases receive treatment. One article mentioned a 17% success rate with treatments however data on treatment outcomes remain sparse and varied at best [(Source)](https://www.psychiatrist.com/jcp/depression/suicide/why-are-outcomes-patients-schizophrenia-poor/). And because of the high rate of comorbidity (rate of occurence with other mental illnesses), schizophrenia remains "poorly understood, and clincially challenging" [(Source)](https://focus.psychiatryonline.org/doi/10.1176/appi.focus.20200026). 

Despite the difficulty in diagnosis, which may be due to a high instance of comorbidity, a lack of a single assessment test, the diagnosis requirements, or its unknown cause, correlates have been defined. "Neuroimaging studies have shown substantive evidence of brain structural, functional and neurochemical alterations in schizophrenia, consistent with the neurodevelopmental and neurodegenerative models of this illness" [(Source)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7724147/). Of note, decreased brain volume has been consistenly defined [(Source)](https://www.tandfonline.com/doi/full/10.1080/09540260701486647?scroll=top&needAccess=true).

Although ML and CNNs are trending in use in neuroimaging, "reliable application of machine learning methods in neuroscience is still in its infancy" [(Source)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6499712/). This may be because ML classifications need to have "translational utility for individual-level predictions" that is "clinically informative, independent of confounding variables, and appropriately assessed for both performance and generalizability" [(Source)](https://www.sciencedirect.com/science/article/abs/pii/S2451902219303040).   
Finally, despite the plethora of material pubished on the brain, the body of literature on functional understanding outside of sensory perceptions (the 5 senses) is still growing [Source](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4975723/).

While there are certainly limitations to present day understanding of the brain and schizophrenia, building a classification model with this mental illness remains a worthwhile endeavor. Specific use cases in practice have the potential to aid diagnosis and further current understanding of the illness. 

## Data Analyzed
* [scans.csv](./data/scans.csv): All images were from the Cobre Study on [COINS](https://coins.trendscenter.org/). In order to gain access, users must register an account with the site and request for both control and schizophrenia groups. 

## Data Dictionary
|Feature|Type|Dataset|Description|
|---|---|---|---|
|patient|str|scans|anonymized patient ID|
|study|str|scans|name of study where patient data originated|
|scan_type|str|scans|type of MRI scan|
|slice|int|scans|slice number of MRI scan|
|schizophrenia|int|scans|diagnosis of schizophrenia, 0 indicates no diagnosis and 1 indicates diagnosis of schizophrenia|


## Analysis, Conclusions, and Recommendations
2 CNNs for particular slice orientations with specific scans were produced (1 T2 model on the tranverse plane and 1 Mprage-T1 model on the sagittal plane). An accuracy score of .8947 for the T2 model with a baseline of .4589 was produced. This model has a sensitivity of .9169 and specificity of .8759. The Mprage model has an accuracy score of .9466 with a baseline of .4979. It has a sensitivity .9504 and specificity of .9428.Both models slightly tended to favor a classification towards schizophrenia. The T2 model tended to misclassify groups at the higher slices (100-120). Upon further investigation, about half of the misclassification of the control group revealed that at higher slices there was white noise i.e scans with no actual brain revealed. No more than 12 misclassified slices per patient was produced. Misclassification of scans for Mprage model was on the exterior portions of the scan (slices below 40 and above 150). Investigation reveals that CNNs were able to classify based on minute brain differences however head shape was also picked up on in constrast of mean images per group. In order to be usable in the field, entire scans per patient can be fed into model and predicted upon. Mean scores of slices can then be generated along side derived confidence intervals to aid with diagnosis. 

The project had several limitation with regards to scope. First, there was a small patient sample size: N=94 for controls and N=83 for schizophrenia. Moreover, not all patients had scans per each scan type and some patients had more than one session scan. There was also a limitation with regards to data and computational power; dicom images store more information (orignally had 150 gbs of data). Model were used on specific machines with specific scan intensities on specific scans on specific planes. Finally, the dataset was not segmented by age or severity of condition.

There is a plethora of options for further investigation both within and outside the project. Within the project the recommendation is to try 3D modeling with derived nii files, accompanied with data augmenation and introduction of GANs. Although adding more data is always an option, using ATS to further model on existing data would be useful. Explanations of the model could also be implemented via gradien ascent and in field applications could be designed with a streamlit app. Outside the project, it is recommend to use fMRIs & clustering models to study brain neural networks. Usage of meta data (age, genetics, and speech) in future models may improve accuracy. Lastly MRI data could be used on other more established mental illnesses or illnesses that are comorbid with schizophrenia

