# Fake News Classifier 

A robust, production-ready Fake News Classification API and Web Application powered by Deep Learning.

This project was built by modularizing a Jupyter Notebook containing an LSTM based classification model into a modern, scalable backend using **FastAPI** and providing a sleek, responsive front-end interface.

##  Features
- **Deep Learning Model**: Utilizes a Bidirectional LSTM constructed with TensorFlow/Keras to analyze linguistic patterns and detect deceptive content.
- **Robust Text Preprocessing**: Incorporates `NLTK` for stopword removal and Porter Stemming, ensuring high-quality tokenization before one-hot encoding.
- **FastAPI Backend**: A high-performance, asynchronous REST API serving both the prediction endpoints and the HTML templates.
- **Premium User Interface**: A meticulously designed vanilla HTML/CSS frontend featuring glassmorphism, fluid animations, and a modern dark aesthetic (no external CSS frameworks).

##  Project Structure
```text
Fake news/
├── src/
│   ├── static/             # CSS & JS assets
│   │   ├── styles.css
│   │   └── script.js
│   ├── templates/          # HTML templates
│   │   └── index.html
│   ├── app.py              # FastAPI Application
│   ├── predict.py          # Prediction Engine & Preprocessing
│   ├── train.py            # Script to train and save the model
│   └── model.h5            # The saved TensorFlow Model (generated after training)
├── requirements.txt        # Python dependencies
├── train.csv               # Dataset used for training (must be placed here)
└── README.md               # Project documentation
```

##  Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Installation
Clone the repository, navigate to the project root, and install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Model Training
Before starting the server, you need to train the LSTM model. Make sure you have the `train.csv` dataset in the root folder, then run:
```bash
python src/train.py
```
This process will preprocess the text, train the sequential model over 10 epochs, and finally generate the `model.h5` inside the `src/` directory.

### 4. Running the Web Application
Once the model is trained, start the FastAPI development server:
```bash
uvicorn src.app:app --reload
```

Then, open your web browser and navigate to:
`http://localhost:8000`

##  How It Works
1. **Input**: A user submits a news title via the web interface.
2. **Preprocessing**: The text is cleaned (non-alphabets removed), lowered, split, stripped of stopwords, and stemmed.
3. **Encoding & Padding**: The processed words are converted to their one-hot representation based on a 5000-word vocabulary, then padded to a uniform sequence length of 20.
4. **Prediction**: The padded sequence is fed into the loaded `model.h5` which outputs a probability metric via a Sigmoid activation function.
5. **Output**: The frontend dynamically updates to showcase whether the headline is deemed "Fake" or "Reliable" along with a confidence percentage.

---

