import uvicorn
from fastapi import FastAPI, HTTPException

import numpy as np
import pickle
import onnxruntime as rt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

app = FastAPI()

# Load the ONNX model
onnx_session = rt.InferenceSession("models/best_model.onnx")

# Load preprocessing transformations from pickle files
with open('models/vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

"""
with open('/models/label_encoder.pkl', 'rb') as label_encoder_file:
    label_encoder = pickle.load(label_encoder_file)
"""

# API Endpoints
@app.get('/')
def index():
    return {'Hello': 'Welcome to IMDb prediction service, access the API docs and test the API at http://0.0.0.0:8000/docs.'}

@app.post('/predict')
async def predict_review(review: str):
    try:
        if not review or not review.strip():
            raise HTTPException(status_code=422, detail="Review cannot be empty")

        # Vectorize the processed review
        review_vectorized = vectorizer.transform([review])
        review_dense = review_vectorized.toarray()

        # Reshape the input to match the expected shape
        review_dense = review_dense.reshape(1, -1)

        # Make predictions using the ONNX model
        input_name = onnx_session.get_inputs()[0].name
        output_name = onnx_session.get_outputs()[0].name
        onnx_input = {input_name: review_dense.astype(np.float32)}
        prediction = onnx_session.run([output_name], onnx_input)[0]

        # Convert the prediction to the original label
        if prediction[0] == 1:
            sentiment = "Positive"  
        else :
            sentiment = "Negative"

        return {"review": review, "sentiment": sentiment}

    except Exception as e:
        error_detail = f"Prediction error: {str(e)}"
        print(f"Exception during prediction: {error_detail}")
        raise HTTPException(status_code=500, detail={"error": error_detail})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
