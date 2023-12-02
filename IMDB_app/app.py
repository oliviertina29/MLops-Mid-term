from flask import Flask, render_template, request
import requests

app = Flask(__name__)

api_route = "http://127.0.0.1:8000"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        review = request.form['review']
        sentiment = "Positif"
        try:    
            # Appel à l'API FastAPI
            response = requests.post(f"{api_route}/predict", data={'review': review})
            result = response.json()

            # Utilisez la clé pour extraire la polarité prédite
            sentiment = result['sentiment']

        except Exception as e:
            error_message = f"Error during API call: {str(e)}"

        return render_template('index.html', review=review, sentiment=sentiment)


if __name__ == '__main__':
    app.run(debug=True, port=8001)
