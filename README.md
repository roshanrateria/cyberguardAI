# CyberguardAI

Welcome to CyberguardAI, a Django-based project focusing on Responsible AI practices to ensure safety, explainability, and multilingual support. This project leverages advanced AI technologies like **Bhasini and Gemini 1.5 pro.**

## Table of Contents
- Overview
- Features
- Setup
- Usage
- Responsible AI Practices
- Contributing
- License

## Overview
CyberguardAI is designed to handle various aspects of cybercrime categorization and reporting. It provides a robust framework for processing and analyzing reports in multiple languages, ensuring user safety, and offering confidence scores for better explainability.

## Features
- **Dynamic Form Handling**: Includes dynamic forms for reporting cybercrimes, which can handle various input types such as text, dates, and file uploads.
- **Multilingual Text AI**: Supports the input and output of multiple languages for complaint filing and processing.
- **Video Complaint Upload**: Allows users to upload complaints as videos. The system extracts audio from videos, converts it to text using Bhasini, and translates it to English.
- **Interactive UI Elements**: Uses JavaScript for interactive UI elements, such as flipping cards and toggling form visibility based on user selections.
- **Detailed Complaint Models**: The `Complain` model includes fields for various aspects of a complaint, such as incident details, financial fraud details, and suspect information.
- **Safety Protocols**: Implements safety protocols to block harmful content and prevent misuse.
- **Confidence Score for Explainability**: Provides confidence scores for AI-generated results to enhance trust and understanding.

## Setup
To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/roshanrateria/cyberguardAI.git
   cd cyberguardAI
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies.

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
1. Access the application at `http://127.0.0.1:8000/`.
2. Navigate through the interface to report and categorize cybercrimes.
3. **Multilingual** support for non-English inputs.
4. **Upload complaint videos; the system will extract, transcribe, and translate the audio**.
5. Review the confidence scores provided for each AI-generated result for better understanding.

## Responsible AI Practices
CyberguardAI emphasizes the following responsible AI practices:
- **Transparency**: Clear documentation and explainability of AI models and results.
- **Safety**: Implementation of safety measures to block harmful content and prevent misuse.
- **Ethical Use**: Adherence to ethical guidelines to ensure AI is used for beneficial purposes.
- **Accountability**: Regular audits and updates to maintain the integrity and reliability of AI systems.
