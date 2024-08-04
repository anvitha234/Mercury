import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load data from CSV
data = pd.read_csv('Responses.csv')

# Define the columns relevant for MBTI determination
questions_mbti = [
    "When working on a project; I prefer to",
    "In social situations; I tend to",
    "When faced with a problem; I usually",
    "When making decisions; I rely more on",
    "In conversations; I tend to focus on",
    "When planning for the future; I",
    "When evaluating a situation; I consider",
    "In conflicts; I tend to",
    "In my daily routine; I prefer",
    "When faced with a deadline; I",
    "In social situations; I tend to"
]

# Ensure the data contains only numeric responses for the questions
responses = data[questions_mbti].apply(pd.to_numeric, errors='coerce').fillna(0).values

# Standardize the input features
scaler = StandardScaler()
responses_scaled = scaler.fit_transform(responses)

# Apply PCA to reduce dimensionality and capture essential patterns
pca = PCA(n_components=10)  # Adjust the number of components based on variance explained
responses_pca = pca.fit_transform(responses_scaled)

# Apply K-Means clustering with 16 clusters (representing 16 MBTI types)
n_clusters = 16
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(responses_pca)

# Validate clustering quality using silhouette score
silhouette_avg = silhouette_score(responses_pca, clusters)
print(f'Silhouette Score: {silhouette_avg}')

# Add the cluster labels to the original data
data['Cluster'] = clusters

# Assume you have a predefined mapping of clusters to MBTI types
# Here we'll just label clusters with arbitrary MBTI types for illustration purposes
# You should replace this with a proper method of determining MBTI type from clusters
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# Map clusters to MBTI types
cluster_to_mbti = {i: mbti_types[i] for i in range(n_clusters)}
data['Predicted MBTI'] = data['Cluster'].map(cluster_to_mbti)

# Save the results to a new CSV file
data.to_csv('Responses_with_Predicted_MBTI.csv', index=False)

print("MBTI personality types have been predicted and saved to 'Responses_with_Predicted_MBTI.csv'.")
