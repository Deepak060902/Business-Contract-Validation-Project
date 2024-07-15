## Introduction

Business contracts are complex legal documents that require thorough review and analysis. Manual review is time-consuming, error-prone, and inconsistent. This project aims to automate the contract validation process using advanced machine learning and natural language processing techniques.

## Features

- **Automated Contract Parsing and Structuring**
- **Clause Classification using Machine Learning**
- **Template Deviation Detection and Highlighting**
- **Summary Generation for Quick Contract Overview**
- **User-friendly Interface for Contract Upload and Result Display**

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Deepak060902/Business-Contract-Validation.git
    cd Business-Contract-Validation
    ```
2. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up the database (MongoDB/MySQL) and update the configuration in the project.

## Usage

1. Start the backend server:
    ```bash
    uvicorn app.main:app --reload
    ```
2. Access the frontend interface (assuming it's served by a different service, update accordingly).

3. Upload contract documents through the interface and view the analysis results.

## Technologies Used

- **Frontend**: ReactJS, Tailwind CSS
- **Backend**: FastAPI
- **Machine Learning**: Python, scikit-learn, TensorFlow, PyTorch
- **NLP**: spaCy, NLTK
- **PDF Processing**: PyPDF2, pdfminer
- **Containerization**: Docker
