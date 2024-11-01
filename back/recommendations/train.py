
import numpy as np
import pandas as pd
import sqlite3

def compute_mse_loss(interaction_matrix_np, predicted_interaction_matrix):
    actual = interaction_matrix_np[interaction_matrix_np > 0]
    predicted = predicted_interaction_matrix[interaction_matrix_np > 0]
    mse_loss = np.mean((actual - predicted) ** 2)
    return mse_loss

def compute_metrics(recommendations, interactions_df, user_id):
   # Get the liked articles
    liked_articles = interactions_df[(interactions_df['user_id'] == user_id) & 
                                     (interactions_df['interaction_value'] == 1.0)]['article_id'].tolist()
    liked_articles_df = articles_df[articles_df['id'].isin(liked_articles)]
    liked_categories = liked_articles_df['category_id'].tolist()

    recommended_articles = recommendations[recommendations['user_id'] == user_id]['article_id'].tolist()
    recommended_articles_df = articles_df[articles_df['id'].isin(recommended_articles)]
    recommended_categories = recommended_articles_df['category_id'].tolist()
    if not liked_articles:  # If no liked articles, precision, recall, F1-score are undefined
        return 0, 0, 0
    # Compute True Positives, False Positives, and False Negatives
    true_positives = len(set(recommended_categories) & set(liked_categories))
    false_positives = len(set(recommended_categories) - set(liked_categories))
    false_negatives = len(set(liked_categories) - set(recommended_categories))
    # print(f'This is true positives {true_positives}')
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1_score


# Connect to your SQLite database
conn = sqlite3.connect('../core.db')
query = """
SELECT interactions.user_id, 
       interactions.article_id, 
       interactions.interaction_value, 
       interactions.interaction_type, 
       interactions.interaction_at,
       uploaded_articles.category_id
FROM interactions
JOIN uploaded_articles
ON interactions.article_id = uploaded_articles.id
"""
# Load the interactions table into a Pandas DataFrame
interactions_df = pd.read_sql_query(query, conn)
articles_df = pd.read_sql_query("SELECT * FROM uploaded_articles", conn)
users_ids = pd.read_sql_query("SELECT id FROM users", conn)
conn.close()
# Create a pivot table to form a user-item interaction matrix
interaction_matrix = interactions_df.pivot_table(
    index='user_id',
    columns='article_id',
    values='interaction_value',
    fill_value=0
)
# unique_article_ids = interactions_df['article_id'].unique()
# print(f"Unique Article IDs in interactions: {len(unique_article_ids)}")
# print(interaction_matrix.shape)
# print("Article IDs in uploaded_articles:", articles_df['id'].unique())
# print("Article IDs in interactions:", unique_article_ids)

all_user_ids = users_ids['id'].unique()
interaction_matrix = interaction_matrix.reindex(all_user_ids, fill_value=0)
num_users, num_articles = interaction_matrix.shape
interaction_matrix_np = interaction_matrix.values

# Define hyperparameters
num_latent_factors = 10 # Number of latent factors
learning_rate = 0.005  # Learning rate
num_epochs = 1000  # Number of epochs
lambda_reg = 0.2  # Regularization parameter
# Original random initialization
user_matrix = np.random.normal(scale=1./num_latent_factors, size=(num_users, num_latent_factors))
article_matrix = np.random.normal(scale=1./num_latent_factors, size=(num_articles, num_latent_factors))
#fill with 0 the users that had no interactions
for user in range(num_users):
    if user not in interactions_df['user_id']:  #
        user_matrix[user] = np.zeros(num_latent_factors)  

category_ids = articles_df['category_id'].unique()
num_categories = len(category_ids)

# Initialize the category matrix
category_matrix = np.random.normal(scale=1. / num_latent_factors, size=(num_categories, num_latent_factors))
# Create a mapping from category_id to its index
category_id_to_index = {category_id: idx for idx, category_id in enumerate(category_ids)}


# Initialize category matrix and map category IDs to indices
num_categories = len(category_ids)  # Number of unique categories
category_matrix = np.random.normal(scale=1. / num_latent_factors, size=(num_categories, num_latent_factors))
category_weight = 5
# Training loop
for epoch in range(num_epochs):
    total_loss = 0  # Track total loss for the epoch
    
    for user in range(num_users):
        for item in range(num_articles):
            if interaction_matrix_np[user, item] > 0:  # Only consider existing interactions
                # Calculate the base prediction (without category contribution)
                predicted_value = np.dot(user_matrix[user, :], article_matrix[item, :].T)
                
                # Get the category of the article
                article_row = articles_df.iloc[item]
                category_id = article_row['category_id']
                category_index = category_id_to_index[category_id]
                
                # Add category contribution to the prediction
                category_contribution = np.dot(category_matrix[category_index], article_matrix[item, :].T)
                predicted_value += category_weight*category_contribution  # Sum of base + category contribution
                
                # Calculate the error
                error = interaction_matrix_np[user, item] - predicted_value
              
                # Update user and item matrices with regularization
                user_matrix[user, :] += learning_rate * (error * article_matrix[item, :] - lambda_reg * user_matrix[user, :])
                article_matrix[item, :] += learning_rate * (error * user_matrix[user, :] - lambda_reg * article_matrix[item, :])
                
                # Update the category matrix
                category_matrix[category_index] += learning_rate * (error * article_matrix[item, :] - lambda_reg * category_matrix[category_index])
                
                # Accumulate loss for the current interaction (Sum of squared errors)
                total_loss += error ** 2  

    # Calculate mean loss for this epoch (only over non-zero interactions)
    mean_loss = total_loss / np.count_nonzero(interaction_matrix_np)
    
    # Predict the interaction matrix for evaluation (over the training set)
    if epoch % 10 == 0:  # Logging every 10 epochs
        predicted_interaction_matrix = np.dot(user_matrix, article_matrix.T)
        mse_loss = compute_mse_loss(interaction_matrix_np, predicted_interaction_matrix)
        print(f"Epoch {epoch + 1}/{num_epochs}, Mean Loss: {mse_loss:.4f}")

# After training, convert the predicted interaction matrix back to a DataFrame
predicted_interaction_df = pd.DataFrame(predicted_interaction_matrix, 
                                         index=interaction_matrix.index, 
                                         columns=interaction_matrix.columns)

# Setting small predicted values to zero
threshold = 1e-10
predicted_interaction_df[predicted_interaction_df < threshold] = 0

# Recommendations
num_recommendations = 5
recommendation_list = []

# Create a mapping from article_id to index for filtering
article_id_mapping = {article_id: idx for idx, article_id in enumerate(articles_df['id'])}

# Recommendations
num_recommendations = 5
recommendation_list = []

for user_id in predicted_interaction_df.index:
    user_predictions = predicted_interaction_df.loc[user_id]
    interacted_articles = interactions_df[interactions_df['user_id'] == user_id]['article_id'].tolist()

    # Create a list of indices for interacted articles
    interacted_indices = [article_id_mapping[article_id] for article_id in interacted_articles if article_id in article_id_mapping]

    # Filter out predictions for interacted articles
    user_predictions_filtered = user_predictions[~user_predictions.index.isin(interacted_indices)]

    # Get top recommendations
    top_recommendations = user_predictions_filtered.nlargest(num_recommendations)

    for article_id in top_recommendations.index:
        predicted_value = top_recommendations[article_id]
        recommendation_list.append({'user_id': user_id, 'article_id': article_id, 'predicted_value': predicted_value})

# After the loop, you can convert recommendation_list to a DataFrame if needed
recommendations_df = pd.DataFrame(recommendation_list)
print(recommendations_df)

# Compute metrics for all users
for user_id in recommendations_df['user_id'].unique():
    precision, recall, f1_score = compute_metrics(recommendations_df, interactions_df, user_id)
    print(f"User {user_id} - Precision: {precision:.4f}, Recall: {recall:.4f}, F1-Score: {f1_score:.4f}")
    
print(article_matrix.shape)
print(user_matrix.shape)

np.save('user_matrix.npy', user_matrix)
np.save('article_matrix.npy', article_matrix)