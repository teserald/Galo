from flask import Flask, render_template
import pandas as pd
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API key
API_KEY = "AIzaSyCszEBggLfAhN87Abl7jw7in605pqhRyb0"  # Your Gemini API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Load the CSV file and extract planet names
def load_planet_names():
    df = pd.read_csv('confirmed_planets_names.csv')
    planet_names = df['pl_name'].tolist()  # 'pl_name' should be the column with planet names
    return planet_names

# Generate planet details using Gemini model
def generate_planet_details(planet_name):
    prompt = f"Provide interesting facts about the {planet_name} which interests a kid and very informative.(reply with plain text)."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating details: {str(e)}"

@app.route('/')
def index():
    planet_names = load_planet_names()
    return render_template('index.html', planet_names=planet_names)

@app.route('/planet/<planet_name>')
def planet(planet_name):
    # Generate details about the planet
    details = generate_planet_details(planet_name)

    # Write the details to a temporary text file
    with open('planet_details.txt', 'w') as f:
        f.write(details)

    # Read from the temporary text file to display in the browser
    with open('planet_details.txt', 'r') as f:
        planet_details = f.read()

    return render_template('planet_details.html', planet_name=planet_name, planet_details=planet_details)

if __name__ == '__main__':
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")  # Open the browser automatically
    app.run(debug=True)