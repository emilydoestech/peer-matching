import pandas as pd
import numpy as np
from fuzzywuzzy import process, fuzz


df = pd.read_csv("patientmatching/data/peerMatchingDf.csv")
phenotypes = pd.read_csv("patientmatching/data/list_of_phenotypes.csv")
df = df.fillna('') #replacing all NaNs with empty strings


# # Jaccard Similarity Score

def JaccardSimilarity(i: set,j: set):
    # we calculate the length of the intersection of i and j
    #  to find the number of shared phenotypes
    emptyVal = ''
    if emptyVal in i:
        i.remove(emptyVal)
    if emptyVal in j:
        j.remove(emptyVal)
    phe_ij = len(i.intersection(j))
    phe_i = len(i) # number of phenotypes for patient i
    phe_j = len(j) # number of phenotypes for patient j
    similarity_ij = phe_ij/(phe_i + phe_j - phe_ij)
    return(similarity_ij)


# # User Matching based on Jaccard

# We can calculate the most similar profiles for a given user and return these
#  profiles (i.e. name, diagnosis status, phenotypes).

def people_like_me(patient, k: int, diagnosis: bin, df):
    # Here we create an empty data frame and np array to allow for
    #  concatination (identity element)
    neighbours = pd.DataFrame()
    similarity = np.empty(0)
    n = 0
    # We convert our phenotypes to sets to use our Jaccard similarity function
    i = set(patient)
    # We loop through to find the similarity of the new patient with each of
    #  the other users in the database
    if diagnosis == True:
        df = df[df.iloc[:,1] != 'undiagnosed']
    for m in range(0, df.index.size):
        # We ignore diagnoses and mames so we can match purely based on symptoms
        j = set(df.iloc[m, 2:df.columns.size])
        similarity_j = [JaccardSimilarity(i,j)]
        similarity = np.append(similarity, similarity_j)
        # Argsort is used to identify users with the highest similarity matches
        sortedSimilarity = np.argsort(similarity)
        # Reversing the order so it shows top matches first
        sortedSimilarity = sortedSimilarity[::-1][:len(sortedSimilarity)]
    # Taking the top k matches
    knn = sortedSimilarity[0:k]
    # Now we know the index for each neighbour. We can use this index to find
    #  the profile for the best matches
    for neighbour in knn:
        neighbourProfile = df.iloc[neighbour,:]
        neighbours = pd.concat([neighbours, neighbourProfile], axis=1)
    return(neighbours.T)


# Convert inputted phenotypes to a uniform list of terminology
def convert_phenotypes(symptoms):
    symptoms = np.array(symptoms)
    newSymptoms = []
    for symptom in symptoms:
        newSymptom, score = process.extractOne(symptom,
                                               phenotypes.values.tolist(),
                                               scorer=fuzz.token_set_ratio)
        newSymptom = ''.join(newSymptom)
        newSymptoms.append(newSymptom)
    return(newSymptoms)
