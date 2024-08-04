import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load data from CSV
data = pd.read_csv('Responses_with_Predicted_MBTI.csv')

# Ensure necessary columns exist and handle categorical data
required_columns = ["Name", "Gender", "Branch", "Field of Study", "Hobbies", "Preferred Language", "Predicted MBTI"]
for col in required_columns:
    if col not in data.columns:
        print(f"Column '{col}' not found in the DataFrame.")
        data[col] = np.nan  # Adding the missing column with NaN values

# Map gender to numeric values
if "Gender" in data.columns:
    data["Gender"] = data["Gender"].map({"Male": 1, "Female": 0}).fillna(-1)

# Convert categorical attributes to numerical codes
categorical_columns = ["Branch", "Field of Study", "Hobbies", "Preferred Language"]
for col in categorical_columns:
    if col in data.columns:
        data[col] = data[col].astype('category').cat.codes

# Define attribute weight mappings for each MBTI type
attribute_weights = {
    "INTJ": {"Gender": 0.05, "Branch": 0.3, "Field of Study": 0.2, "Hobbies": 0.2, "Preferred Language": 0.25},
    "INTP": {"Gender": 0.05, "Branch": 0.25, "Field of Study": 0.25, "Hobbies": 0.2, "Preferred Language": 0.25},
    "ENTJ": {"Gender": 0.05, "Branch": 0.3, "Field of Study": 0.2, "Hobbies": 0.2, "Preferred Language": 0.25},
    "ENTP": {"Gender": 0.05, "Branch": 0.25, "Field of Study": 0.25, "Hobbies": 0.2, "Preferred Language": 0.25},
    "INFJ": {"Gender": 0.05, "Branch": 0.3, "Field of Study": 0.2, "Hobbies": 0.2, "Preferred Language": 0.25},
    "INFP": {"Gender": 0.05, "Branch": 0.25, "Field of Study": 0.25, "Hobbies": 0.2, "Preferred Language": 0.25},
    "ENFJ": {"Gender": 0.05, "Branch": 0.3, "Field of Study": 0.2, "Hobbies": 0.2, "Preferred Language": 0.25},
    "ENFP": {"Gender": 0.05, "Branch": 0.25, "Field of Study": 0.25, "Hobbies": 0.2, "Preferred Language": 0.25},
    "ISTJ": {"Gender": 0.05, "Branch": 0.3, "Field of Study": 0.2, "Hobbies": 0.2, "Preferred Language": 0.25},
    "ISFJ": {"Gender": 0.05, "Branch": 0.3, "Field of Study": 0.2, "Hobbies": 0.2, "Preferred Language": 0.25},
    "ESTJ": {"Gender": 0.05, "Branch": 0.3, "Field of Study": 0.2, "Hobbies": 0.2, "Preferred Language": 0.25},
    "ESFJ": {"Gender": 0.05, "Branch": 0.3, "Field of Study": 0.2, "Hobbies": 0.2, "Preferred Language": 0.25},
    "ISTP": {"Gender": 0.05, "Branch": 0.25, "Field of Study": 0.25, "Hobbies": 0.2, "Preferred Language": 0.25},
    "ISFP": {"Gender": 0.05, "Branch": 0.25, "Field of Study": 0.25, "Hobbies": 0.2, "Preferred Language": 0.25},
    "ESTP": {"Gender": 0.05, "Branch": 0.25, "Field of Study": 0.25, "Hobbies": 0.2, "Preferred Language": 0.25},
    "ESFP": {"Gender": 0.05, "Branch": 0.25, "Field of Study": 0.25, "Hobbies": 0.2, "Preferred Language": 0.25},
}

# Compute vector embeddings based on attributes
def compute_embeddings(data, attribute_weights):
    embeddings = []
    for index, row in data.iterrows():
        mbti_type = row["Predicted MBTI"]
        attr_weights = attribute_weights.get(mbti_type, {k: 0 for k in ["Gender", "Branch", "Field of Study", "Hobbies", "Preferred Language"]})
        
        attr_embedding = np.array([row.get(attr, 0) * attr_weights.get(attr, 0) for attr in ["Gender", "Branch", "Field of Study", "Hobbies", "Preferred Language"]])
        
        embeddings.append(attr_embedding)
    return np.array(embeddings)

embeddings = compute_embeddings(data, attribute_weights)

# Calculate cosine similarity between all pairs
similarity_matrix = cosine_similarity(embeddings)

# Function to generate unique names
def generate_unique_name(existing_names, index):
    return f"User_{index + 1}"

# Generate top 3 matches for each individual
top_matches = {}
for idx, row in data.iterrows():
    similarity_scores = similarity_matrix[idx]
    sorted_indices = np.argsort(similarity_scores)[::-1]  # Sort by similarity score in descending order
    top_indices = [i for i in sorted_indices if i != idx][:3]  # Exclude the individual themselves and get top 3 matches
    
    if len(top_indices) < 3:
        # Ensure at least one match is available
        top_indices.extend([i for i in sorted_indices if i != idx][3:4])
    
    match_names = []
    for match_idx in top_indices:
        match_name = data.iloc[match_idx]['Name']
        if pd.isna(match_name) or match_name == '':
            match_name = generate_unique_name(data['Name'].tolist(), match_idx)
            data.at[match_idx, 'Name'] = match_name  # Update the name in the DataFrame
        
        match_names.append(match_name)
    
    top_matches[row['Name']] = match_names

# Add top matches to the DataFrame
data["Top Matches"] = data["Name"].map(top_matches)

# Save the results to a new CSV file
data.to_csv('Responses_Matches.csv', index=False)

print("Top matches have been generated and saved to 'Responses_Matches.csv'.")
