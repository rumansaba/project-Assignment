from flask import Flask, render_template, request

app = Flask(__name__)

# Sample data representing items and their features
items = {
    'item1': {'name': 'Item 1', 'category': 'Category A', 'price': 20},
    'item2': {'name': 'Item 2', 'category': 'Category B', 'price': 30},
    'item3': {'name': 'Item 3', 'category': 'Category A', 'price': 25},
    # Add more items as needed
}

# Function to recommend items based on user preferences
def recommend_items(user_preferences):
    # For simplicity, the recommendation is based on the item category
    recommended_items = []
    for item_id, item_data in items.items():
        if item_data['category'] in user_preferences:
            recommended_items.append(item_data)
    return recommended_items

@app.route('/')
def index():
    return render_template('index.html', items=items)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_preferences = request.form.getlist('category')
    recommended_items = recommend_items(user_preferences)
    return render_template('recommendation.html', recommended_items=recommended_items)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
