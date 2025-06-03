import pathlib
import google.generativeai as genai
from PIL import Image

def init_gemini(api_key: str):
    """Initialize Gemini API with the provided API key"""
    genai.configure(api_key=api_key)

def analyze_chart(image_path: str) -> str:
    """
    Send the chart image to Gemini for analysis
    Returns the interpretation as text
    """
    try:
        # Get the Gemini Pro Vision model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Load the image
        image = Image.open(image_path)
        
        # Prepare the prompt
        prompt = """
        Please analyze this financial chart and provide insights about:
        1. Key support and resistance levels
        2. Major trend directions
        3. Any notable breakout points
        4. Overall market sentiment based on the patterns
        Be specific about price levels and dates where possible.
        """
        
        # Generate content
        response = model.generate_content([prompt, image])
        
        return response.text
        
    except Exception as e:
        return f"Error analyzing chart: {str(e)}"
