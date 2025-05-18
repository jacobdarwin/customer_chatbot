import json
import random
import nltk
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

nltk.download('punkt')

# Load intents
with open("intents.json") as f:
    data = json.load(f)

# Prepare training data
corpus = []
tags = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        corpus.append(pattern)
        tags.append(intent['tag'])

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus).toarray()
model = LogisticRegression()
model.fit(X, tags)

# Load orders CSV
orders_df = pd.read_csv("orders.csv")

# Load products CSV
products_df = pd.read_csv("products.csv")

def predict_tag(user_input):
    user_input_vector = vectorizer.transform([user_input]).toarray()
    probs = model.predict_proba(user_input_vector)[0]
    max_prob = np.max(probs)
    tag = model.classes_[np.argmax(probs)]
    return tag if max_prob > np.mean(probs) else None

def get_response(tag, user_input=None):
    if tag == "order_status" and user_input:
        order_id = next((word for word in user_input.split() if word.startswith("ORD")), None)
        if order_id:
            return get_order_status(order_id)
        else:
            return "Please provide your order ID to check its status."

    if tag == "product_info" and user_input:
        product_name = user_input.split()[-1]  # Extract product name
        response = get_product_info(product_name)
        return response

    for intent in data['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

def get_order_status(order_id):
    try:
        order_info = orders_df[orders_df["order_id"] == order_id]
        if not order_info.empty:
            product = order_info.iloc[0]["product_name"]
            status = order_info.iloc[0]["status"]
            delivery_date = order_info.iloc[0]["expected_delivery_date"]
            amount = order_info.iloc[0]["amount"]

            response = f"**Order Details:**\n"
            response += f"🆔 **Order ID:** {order_id}\n"
            response += f"📦 **Product:** {product}\n"
            response += f"📌 **Status:** {status}\n"
            if pd.notna(delivery_date):
                response += f"🚚 **Expected Delivery:** {delivery_date}\n"
            if pd.notna(amount):
                response += f"💰 **Amount Paid:** ₹{amount}\n"
            
            return response.strip()
        else:
            return "⚠️ Order ID not found. Please check and try again."
    except Exception as e:
        return f"❌ Error retrieving order information: {e}"

def get_product_info(query):
    try:
        product_info = products_df[
            (products_df["product_name"].str.contains(query, case=False, na=False)) | 
            (products_df["product_id"] == query)
        ]
        if not product_info.empty:
            response = f"**Product Details:**\n"
            response += f"🆔 **Product ID:** {product_info.iloc[0]['product_id']}\n"
            response += f"📦 **Product:** {product_info.iloc[0]['product_name']}\n"
            response += f"💰 **Price:** ₹{product_info.iloc[0]['price']}\n"
            response += f"📌 **Availability:** {product_info.iloc[0]['availability']}\n"
            response += f"📝 **Description:** {product_info.iloc[0]['description']}\n"
            return response.strip()
        else:
            return "Sorry, I couldn't find details for that product. Please check the name or product ID."
    except Exception as e:
        return f"Error retrieving product information: {e}"