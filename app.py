import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os
import zipfile
from io import StringIO

# Custom font path
font_path = 'font/Avenir/Avenir Black/Avenir Black.ttf'
custom_font = FontProperties(fname=font_path)

# Function to plot each subplot
def plot_subplot(data, title, subplot_position, aligned_models, aligned_colors, highlighted_list):
    plt.subplot(2, 2, subplot_position)
    bars = plt.bar(aligned_models, data, color=aligned_colors, width=0.7)
    plt.xticks([])  # Remove x-axis
    plt.yticks([])  # Remove y-axis
    plt.box(False)  # Hide box
    plt.grid(False)
    plt.text(0.5, -0.15, title, ha='center', transform=plt.gca().transAxes, fontproperties=custom_font)
    for bar, value, model in zip(bars, data, aligned_models):
        alpha_value = 1 if model in highlighted_list else 0.1
        plt.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.5,
                 f'{value}%',
                 ha='center',
                 color=aligned_colors[aligned_models.index(model)],
                 fontsize=15,
                 fontproperties=custom_font,
                 alpha=alpha_value)
        bar.set_alpha(alpha_value)

# Initialize Streamlit app
st.title("Dynamic Bar Chart for Model Comparison")

# Allow user to change the image titles
title1 = st.text_input("Title for the first image:", "Correcting Precision")
title2 = st.text_input("Title for the second image:", "Correcting Recall")

# Upload CSV or copy-paste table
data_source = st.selectbox("How would you like to input data?", ["Copy-Paste Table", "Upload CSV"])

if data_source == "Copy-Paste Table":
    table_data = st.text_area("Paste your table here (Tab or comma-separated)", '''Model,Correcting Precision,Correcting Recall,Color
Rule Based Model,65.96,56.35,#6e13a5
Mix Teacher Transformer (MMT),57.04,57.19,#eb8b33
MTT-augmented,66.97,60.80,#8b1c45
MTT-augmented (pass@10),79.62,72.28,#377e22
Pure-heuristic Transformer (CnG),64.02,54.03,#3880f2
MTT-augmented (Tiny),50.98,33.40,#100198
Jamspell,29.84,18.18,#f6ce7f
''')
    table = pd.read_csv(StringIO(table_data), sep=',|\t', engine='python')
else:
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        table = pd.read_csv(uploaded_file)

# Display table
if table is not None:
    st.write("Data Table")
    st.write(table)

    # Extract data
    models = list(table["Model"])
    correcting_precision = list(table["Correcting Precision"])
    correcting_recall = list(table["Correcting Recall"])
    custom_colors = list(table["Color"])

    # Highlighted models
    highlighted_list = st.multiselect("Select models to highlight", models, models)

    # Sort data by Correcting Precision
    sorted_data_by_precision = sorted(zip(correcting_precision, correcting_recall, models, custom_colors), key=lambda x: x[0])
    sorted_correcting_precision, aligned_correcting_recall, aligned_models, aligned_colors = zip(*sorted_data_by_precision)

    # Create figure
    fig = plt.figure(figsize=(18, 9))

    # Plot Correcting Precision on the bottom left
    plot_subplot(sorted_correcting_precision, title1, 1, aligned_models, aligned_colors, highlighted_list)

    # Plot Correcting Recall on the bottom right
    plot_subplot(aligned_correcting_recall, title2, 2, aligned_models, aligned_colors, highlighted_list)

    st.pyplot(fig)
