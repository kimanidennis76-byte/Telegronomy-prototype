# Telegronomy Prototype

**AI-Powered Agricultural Intelligence for Farmers**

Telegronomy is an agricultural technology prototype designed to help farmers turn crop observations into actionable agricultural intelligence while connecting them with professional agronomic support.

# The Problem

Farmers can struggle to identify crop diseases early and access practical, reliable agricultural guidance when problems occur.

Traditional agricultural support can also be difficult to access at the moment a farmer needs it.

# The Solution

Telegronomy demonstrates an end-to-end digital workflow that allows a farmer to:

* Create and manage a farm
* Add fields and crops
* Record crop health information
* Upload crop photographs
* Use an AI model to identify selected onion diseases
* Receive disease-specific management guidance
* Review previous disease assessments
* Consult an agronomist
* Receive professional agronomic feedback
* Maintain a Digital Farm Passport containing the farmer's agricultural records

The prototype combines **AI-assisted disease detection with human agronomic support**, rather than treating AI as a replacement for agricultural professionals.

# How It Works

The core farmer workflow is:

    text
Farmer
   ↓
Farm
   ↓
Field
   ↓
Crop
   ↓
Crop Health
   ↓
Crop Photograph
   ↓
AI Disease Detection
   ↓
Disease Assessment & Management Guidance
   ↓
Agronomist Consultation
   ↓
Digital Farm Passport


# AI / Machine Learning

The prototype includes a trained image-classification model for onion disease detection.

## Model

* **Architecture:** MobileNetV3 Small
* **Framework:** PyTorch
* **Image size:** 224 × 224
* **Classes:** 4
* **Training environment:** CPU
* **Model version:** Telegronomy Onion AI v1.0

# Supported Onion Classes

1. Healthy
2. Iris Yellow Virus
3. Leaf Blight
4. Purple Blotch

## Prototype Test Result

The trained model achieved approximately **85% accuracy on the held-out test set**.

### Class-level test performance

| Class             | Test Accuracy |
| ----------------- | ------------: |
| Healthy           |        87.69% |
| Iris Yellow Virus |        86.05% |
| Leaf Blight       |        73.33% |
| Purple Blotch     |        75.00% |

These results are presented as **prototype model performance**, not as evidence of production-level agricultural diagnostic reliability.

# Technology Stack

* Python
* Streamlit
* PyTorch
* Torchvision
* SQLite
* PIL / image processing
* Git
* GitHub

# Prototype Features

## Farmer System

* User registration and login
* Farm management
* Field management
* Crop management
* Crop health assessment
* AI disease detection
* Disease assessment history
* Agronomist consultation
* Digital Farm Passport

## Agronomist System

* Consultation dashboard
* Consultation review
* Professional response
* Management advice
* Follow-up recommendation

# Project Structure

    text
telegronomy/
│
├── ai/
│   └── disease_ai.py
│
├── backend/
│   └── main.py
│
├── database/
│   └── database.py
│
├── decision_engine/
│   └── engine.py
│
├── frontend/
│   ├── app.py
│   └── pages/
│       ├── agronomist_dashboard.py
│       ├── crop_health.py
│       ├── crops.py
│       ├── disease_detection.py
│       ├── disease_history.py
│       ├── farm_passport.py
│       ├── farmer_dashboard.py
│       ├── fields.py
│       └── my_farm.py
│
├── ML/
│   ├── evaluation/
│   ├── inference/
│   ├── models/
│   ├── training/
│   └── dataset/
│
├── requirements.txt
├── .gitignore
└── README.md


The dataset and local database are excluded from version control.

# Running the Prototype

## 1. Clone the repository

    bash
git clone git@github.com:kimanidennis76-byte/Telegronomy-prototype.git
cd telegronomy-prototype


## 2. Create a virtual environment

    bash
python -m venv venv


## 3. Activate the environment

On Windows:

    powershell
venv\Scripts\activate


## 4. Install dependencies
    bash
pip install -r requirements.txt


## 5. Run the Streamlit application

    bash
streamlit run frontend/app.py


The application will open in your browser.

# Prototype Results

The prototype demonstrates a complete working agricultural intelligence workflow rather than an isolated machine-learning experiment.

A farmer can move from:

**Farm → Field → Crop → Crop Health → AI Disease Detection → Disease History → Agronomist Consultation → Digital Farm Passport**

The project therefore demonstrates both the **technical AI capability** and the **user workflow surrounding that capability**.

# Future Development

This repository represents the **Telegronomy Prototype**.

The next stage will be a separate production-oriented MVP built from scratch.

## Future platform expansion includes:

* Expanded crop and disease coverage
* Production-grade system architecture
* Dedicated farmer application
* Agronomist portal
* Agrovet portal
* Extension Officer portal
* Administration system
* Digital Farm Passport expansion
* Agricultural decision engine
* Weather and maps integration
* Notifications
* Production security
* Data protection and governance
* Cloud deployment
* Monitoring and maintenance

The prototype demonstrates the core intelligence and farmer workflow. The broader agricultural ecosystem represents the next phase of Telegronomy's development.

# Why This Project

Telegronomy explores how artificial intelligence can be combined with agricultural expertise to make crop health information more accessible to farmers.

The core principle is simple:

> **AI can help identify the problem. Agricultural professionals help guide the solution.**

# Author

**Dennis Kimani**

Telegronomy — AI-Powered Agricultural Intelligence

**Project status:** Prototype / Proof of Concept
