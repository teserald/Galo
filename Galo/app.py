from flask import Flask, render_template
import pandas as pd
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API key
API_KEY = "AIzaSyCszEBggLfAhN87Abl7jw7in605pqhRyb0"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Update the CSV file with wget
def update_csv():
    print("Updating confirmed_planets_names.csv with the latest data...")
    os.system('wget "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name+from+pscomppars&format=csv" -O "confirmed_planets_names.csv"')

# Load the CSV file and extract planet names
def load_planet_names():
    update_csv()  # Update the CSV on app start
    df = pd.read_csv('confirmed_planets_names.csv')
    planet_names = df['pl_name'].tolist()
    return planet_names

# Generate planet details using Gemini model
def generate_planet_details(planet_name):
    prompt = f"Provide interesting facts about the {planet_name} which even interests even a kid and very informative(strictly include how it is found, about host star, mass, density, distance from us, radius dustance from its star, etc)(strictly reply with plain text only, espacially never generate bold text)(only refer to https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+pscomppars&format=csv) ."
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
    details = generate_planet_details(planet_name)
    with open('planet_details.txt', 'w') as f:
        f.write(details)
    with open('planet_details.txt', 'r') as f:
        planet_details = f.read()
    return render_template('planet_details.html', planet_name=planet_name, planet_details=planet_details)

if __name__ == '__main__':
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
