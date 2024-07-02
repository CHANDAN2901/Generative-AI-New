# AI Content Generator

This Streamlit app generates content using CrewAI and HuggingFace models.

## Requirements

- Python 3.7+
- Streamlit
- CrewAI
- Langchain Community
- python-dotenv
- HuggingFace account and API key

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Generative-AI.git
   cd Generative-AI/AI-Content-Generator
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory and add your HuggingFace API key:
   ```
   HUGGINGFACE_API_KEY=your_api_key_here
   ```

## Running the App

To run the Streamlit app, use the following command:

```
streamlit run app.py
```

The app will open in your default web browser. Enter a topic for content generation and click the "Generate Content" button.

## Note

Ensure that your `.env` file is included in your `.gitignore` to avoid accidentally sharing your API key.