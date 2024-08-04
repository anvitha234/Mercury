import pandas as pd

# Load the dataset
df = pd.read_csv('MentorPred.csv')

# Function to create sets of individuals
def create_mentor_sets(df):
    want_mentor = df[df['H Mentor'] == 'Yes']
    want_to_be_mentor = df[df['B Mentor'] == 'Yes']
    return want_mentor, want_to_be_mentor

# Function to calculate the score for matching
def calculate_score(mentee, mentor):
    score = 0

    # Static weightages
    weights = {
        'background': 0.3,
        'year_of_study': 0.25,
        'mbti': 0.25,
        'branch': 0.1,
        'preferred_language': 0.05,
        'gender': 0.05
    }

    # Background preference
    if mentee['background'] == "Same Gender" and mentee['Gender'] == mentor['Gender']:
        score += weights['background']
    elif mentee['background'] == "Preferred Language" and mentee['Preferred Language'] == mentor['Preferred Language']:
        score += weights['background']
    elif mentee['background'] == "Different Languages" and mentee['Preferred Language'] != mentor['Preferred Language']:
        score += weights['background']
    elif mentee['background'] == 0:
        score += weights['background']

    # Year of Study
    if mentor['Year of Study'] > mentee['Year of Study']:
        score += weights['year_of_study']

    # MBTI
    if mentee['MBTI'] == mentor['MBTI']:
        score += weights['mbti']

    # Branch
    if mentee['Branch'] == mentor['Branch']:
        score += weights['branch']

    # Preferred Language
    if mentee['Preferred Language'] == mentor['Preferred Language']:
        score += weights['preferred_language']

    # Gender
    if mentee['Gender'] == mentor['Gender']:
        score += weights['gender']

    return score

# Function to match mentors with mentees based on criteria
def match_mentors(mentees, mentors):
    # Create an empty DataFrame to hold matches
    matches_df = pd.DataFrame(columns=['Mentee', 'Mentor1', 'Mentor2'])
    assigned_mentors = set()  # Track assigned mentors to avoid reciprocal assignments

    for _, mentee in mentees.iterrows():
        potential_matches = mentors.copy()

        # Remove mentees who are trying to mentor themselves
        potential_matches = potential_matches[potential_matches['Name'] != mentee['Name']]

        # Remove potential mentors who are already assigned to someone else
        potential_matches = potential_matches[~potential_matches['Name'].isin(assigned_mentors)]

        # Calculate scores for potential matches
        potential_matches['score'] = potential_matches.apply(lambda x: calculate_score(mentee, x), axis=1)

        # Sort potential matches by score in descending order
        potential_matches = potential_matches.sort_values(by='score', ascending=False)

        # Select the top 2 matches
        top_matches = potential_matches.head(2)

        if not top_matches.empty:
            match_info = top_matches['Name'].tolist()
            while len(match_info) < 2:
                match_info._append(f"Auto-generated Name {len(match_info)+1}")

            # Record the match and update the assigned mentors set
            for mentor in match_info:
                assigned_mentors.add(mentor)
                
            # Append the match to the DataFrame
            matches_df = matches_df._append({
                'Mentee': mentee['Name'],
                'Mentor1': match_info[0],
                'Mentor2': match_info[1]
            }, ignore_index=True)

    return matches_df

# Generate the sets of mentees and mentors
mentees, mentors = create_mentor_sets(df)

# Match mentees with mentors
match_results_df = match_mentors(mentees, mentors)

# Save the match results to a CSV file
match_results_df.to_csv('MentorPred_Res.csv', index=False)

print("Mentor match results have been saved to 'MentorPred_Res.csv'.")
