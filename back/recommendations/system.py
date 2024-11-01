import numpy as np
import pandas as pd
import sqlite3
import os
def get_recommendations_for_user(user_id, num_recommendations=6):
    # Load the saved latent matrices
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'user_matrix.npy')
    file_path0 = os.path.join(script_dir, 'article_matrix.npy')
    user_matrix = np.load(file_path)
    article_matrix = np.load(file_path0)

    # print(f"Article Matrix Shape: {article_matrix.shape}")

    # Compute the predicted interaction values for the user
    if user_id >= user_matrix.shape[0]:
        new_row = np.zeros(10)
        user_matrix = np.vstack([user_matrix, new_row])

    user_index = user_id - 1  # Assuming user_id is the same as the index; adjust if needed
    predicted_values = np.dot(user_matrix[user_index], article_matrix.T)

    # Load interaction data to filter out already interacted articles
    db_path = os.path.join(script_dir, '../core.db')
    conn = sqlite3.connect(db_path)
    connections_df = pd.read_sql_query(
    """
    SELECT DISTINCT u.id 
    FROM connections c 
    JOIN users u ON (c.receiver = u.id OR c.sender = u.id) 
    WHERE (c.sender = ? OR c.receiver = ?) AND u.id != ?
    """, 
    conn, 
    params=(user_id, user_id, user_id)
)

    interactions_df = pd.read_sql_query("SELECT * FROM interactions WHERE user_id = ?", conn, params=(user_id,))
    # Get interacted articles
    interacted_articles = interactions_df['article_id'].tolist()
    connection_recommendations = []

    # Loop through connections to get their interacted articles
    for _, row in connections_df.iterrows():
        connected_user_id = row['id']
        connected_interactions_df = pd.read_sql_query("SELECT * FROM interactions WHERE user_id = ?", conn, params=(connected_user_id,))
        connected_interacted_articles = connected_interactions_df['article_id'].tolist()
        
        for article_id in connected_interacted_articles:
            if article_id not in interacted_articles:
                # This could be a more sophisticated scoring system based on your needs
                connection_recommendations.append((article_id, predicted_values[article_id]))  # Using predicted value as score

    # Get unique recommendations and sort them
    connection_recommendations = list(set(connection_recommendations))
    connection_recommendations.sort(key=lambda x: x[1], reverse=True)

    # Combine with original predictions
    combined_recommendations = list(zip(range(len(predicted_values)), predicted_values)) + connection_recommendations

    # Exclude already interacted articles
    combined_recommendations = [(article_id, score) for article_id, score in combined_recommendations if article_id not in interacted_articles]
    top_recommendations = sorted(combined_recommendations, key=lambda x: x[1], reverse=True)[:num_recommendations]

    # Format the recommendations for output
    recommendations_df = pd.DataFrame(top_recommendations, columns=['article_id', 'predicted_value'])
    
    
    conn.close()

    return recommendations_df['article_id']

