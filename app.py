# -*- coding: utf-8 -*-
"""app.py.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GC5QPDRKdqHdxLKN9copjAYklkiIeQFi

**vdr.app.py**
"""


import streamlit as st
from multiapp import MultiApp
from apps import home, data, model # import your app modules here
import pandas as pd
from PIL import Image
import subprocess
import os
import pybase64
import pickleshare


# Create a page dropdown 
page = st.selectbox("Choose your page", ["Page 1", "Page 2", "Page 3"])

if page =="Page 1":
  # Display details of page 1





# Molecular descriptor calculator
def desc_calc():
    # Performs the descriptor calculation
    bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    os.remove('molecule.smi')

# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

# Model building
def build_model(input_data):
    # Reads in saved regression model
    load_model = pickle.load(open('vdr_model.pkl', 'rb'))
    # Apply model to make predictions
    prediction = load_model.predict(input_data)
    st.header('**Prediction output**')
    prediction_output = pd.Series(prediction, name='pIC50')
    molecule_name = pd.Series(load_data[1], name='molecule_name')
    df = pd.concat([molecule_name, prediction_output], axis=1)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)

# Logo image
image = Image.open('logo1a.jpg')

st.image(image, use_column_width=True)

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Submission", submission.app)
app.add_app("Help", help.app)
app.add_app("Method", method.app)
app.add_app("Team", team.app)

# The main app
app.run()



# Page title
st.markdown("""

Vitamin D Receptor (VDR) is a drug target for many infectious and immunological diseases. VDR-Pred tool employs to predict VDR agonistic activity of drug-like molecules using Machine learning algorithm-based QSAR models.
The screening results allow the user to use the predicted molecules to activate the vitamin D receptor enzyme. 

**Credits**
- App built in `Python` + `Streamlit` by [Gurudeeban Selvaraj], Centre for Research in Molecular Modeling (CERMM), Concordia University, Montreal, Quebec, Canada, H4B 1R6 
- Descriptor calculated using [PaDEL-Descriptor](http://www.yapcwsoft.com/dd/padeldescriptor/) [[Read the Paper]](https://doi.org/10.1002/jcc.21707).

---
""")

# Sidebar
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input file", type=['txt'])
    st.sidebar.markdown("""
[Example input file](https://github.com/Gurudeeban-Selvaraj/advanced-therapeutics/blob/main/example.txt)
""")

if st.sidebar.button('Predict'):
    load_data = pd.read_table(uploaded_file, sep=' ', header=None)
    load_data.to_csv('molecule.smi', sep = '\t', header = False, index = False)

    st.header('**Original input data**')
    st.write(load_data)
    
    with st.spinner("Calculating descriptors..."):
        desc_calc()
        
    # Read in calculated descriptors and display the dataframe
    st.header('**Calculated molecular descriptors**')
    desc = pd.read_csv('descriptors_output.csv')
    st.write(desc)
    st.write(desc.shape)

    # Read descriptor list used in previously built model
    st.header('**Subset of descriptors from previously built models**')
    Xlist = list(pd.read_csv('descriptor_list.csv').columns)
    desc_subset = desc[Xlist]
    st.write(desc_subset)
    st.write(desc_subset.shape)
    # Apply trained model to make prediction on query compounds
    build_model(desc_subset)
else:
    st.info('Upload input data in the sidebar to start!')
