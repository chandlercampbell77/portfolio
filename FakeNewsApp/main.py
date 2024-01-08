import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import re
import logging
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to load and preprocess data from Kaggle dataset
# Collected or Available Datasets
def load_and_preprocess_data():
    real_news = pd.read_csv('True.csv')
    fake_news = pd.read_csv('Fake.csv')

    real_news['label'] = 0
    fake_news['label'] = 1

    real_news['combined'] = real_news['title'] + ' ' + real_news['text']
    fake_news['combined'] = fake_news['title'] + ' ' + fake_news['text']

    return pd.concat([real_news, fake_news])

# Function to generate and save a word cloud
def generate_and_save_wordcloud(text, filename):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(filename)
    plt.close()

# Function to calculate average word count
def avg_word_count(texts):
    return texts.apply(lambda x: len(x.split())).mean()

# Function to create and save bar chart
def create_bar_chart(real_news, fake_news):
    avg_real_words = avg_word_count(real_news['text'])
    avg_fake_words = avg_word_count(fake_news['text'])

    plt.bar(['Real News', 'Fake News'], [avg_real_words, avg_fake_words], color=['blue', 'red'])
    plt.xlabel('Category')
    plt.ylabel('Average Word Count')
    plt.title('Average Word Count in Real News vs Fake News')
    plt.savefig('word_count_bar_chart.png')
    plt.close()

# Industry-Appropriate Security Features using input validation
def validate_input(text):
    # Remove special characters, keep only alphanumeric and spaces
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    text = text.lower().strip()
    return text

# Function to check news title using the model
def check_news_title():
    user_input_title = title_entry.get()
    user_input_title = validate_input(user_input_title)

    if user_input_title:
        user_input_title_vec = vectorizer.transform([user_input_title])
        probabilities = classifier.predict_proba(user_input_title_vec)
        fake_prob = probabilities[0][1]

        prediction = ""
        if fake_prob > 0.8:
            prediction = f"Very likely to be fake (Probability: {fake_prob:.2f})"
        elif 0.5 < fake_prob <= 0.8:
            prediction = f"Likely to be fake (Probability: {fake_prob:.2f})"
        elif 0.2 < fake_prob <= 0.5:
            prediction = f"Might be fake (Probability: {fake_prob:.2f})"
        else:
            prediction = f"Unlikely to be fake (Probability: {fake_prob:.2f})"

        messagebox.showinfo("Result", prediction)
        # Log user input and prediction
        logging.info(f"User Input: '{user_input_title}' | Prediction: {prediction}")

# Function to load and resize an image
def load_resized_image(path, size):
    image = Image.open(path)
    resized_image = image.resize(size)
    return ImageTk.PhotoImage(resized_image)

# Main function
def main():
    global vectorizer, classifier, title_entry

    # Setup logging
    # Tools to Monitor and Maintain the Product
    logging.basicConfig(filename='user_predictions.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    # Load and preprocess data
    data = load_and_preprocess_data()

    real_news = data[data['label'] == 0]
    fake_news = data[data['label'] == 1]

    # Generate and save word clouds and bar chart
    # Descriptive Method
    # Methods and Algorithms Supporting Data Exploration and Preparation
    # Data Visualization Functionalities
    generate_and_save_wordcloud(' '.join(real_news['text']), 'real_news_wordcloud.png')
    generate_and_save_wordcloud(' '.join(fake_news['text']), 'fake_news_wordcloud.png')
    create_bar_chart(real_news, fake_news)

    # Data preprocessing and feature extraction
    # Predictive Method
    # Ability to Support Featurizing, Parsing, Cleaning, and Wrangling Datasets
    vectorizer = CountVectorizer(stop_words='english', ngram_range=(1, 2), max_features=1000)
    all_features = vectorizer.fit_transform(data['combined'])
    X_train, X_test, y_train, y_test = train_test_split(all_features, data['label'], test_size=0.2, random_state=42)

    # Model training and metrics calculation
    # Implementation of Machine-Learning Methods and Algorithms
    classifier = MultinomialNB(alpha=0.1)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    # Functionalities to Evaluate the Accuracy of the Data Product
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Tkinter GUI Setup
    # A User-Friendly, Functional Dashboard with Three Visualization Types
    root = tk.Tk()
    root.title("Fake News Detector")

    # Display model metrics
    metrics_text = f"Model Accuracy: {accuracy:.2f}\nRecall: {recall:.2f}\nPrecision: {precision:.2f}\nF1 Score: {f1:.2f}"
    metrics_label = tk.Label(root, text=metrics_text)
    metrics_label.pack()

    # Decision Support Functionality
    # Implementation of Interactive Queries
    tk.Label(root, text="Enter a news title to check:").pack()
    title_entry = tk.Entry(root)
    title_entry.pack()
    tk.Button(root, text="Check", command=check_news_title).pack()

    # Specify desired size (width, height)
    desired_size = (300, 150)

    # Load and display resized images with labels
    real_wc_img = load_resized_image('real_news_wordcloud.png', desired_size)
    real_wc_label = tk.Label(root, image=real_wc_img)
    real_wc_label.pack()
    real_wc_text_label = tk.Label(root, text="Real News Word Cloud")
    real_wc_text_label.pack()

    fake_wc_img = load_resized_image('fake_news_wordcloud.png', desired_size)
    fake_wc_label = tk.Label(root, image=fake_wc_img)
    fake_wc_label.pack()
    fake_wc_text_label = tk.Label(root, text="Fake News Word Cloud")
    fake_wc_text_label.pack()

    bar_chart_img = load_resized_image('word_count_bar_chart.png', desired_size)
    bar_chart_label = tk.Label(root, image=bar_chart_img)
    bar_chart_label.pack()
    bar_chart_text_label = tk.Label(root, text="Word Count Comparison")
    bar_chart_text_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
