import joblib

class SVMModel:
    def __init__(self, model_name):
        # Load the pre-trained model and TF-IDF vectorizer
        # Load the model and vectorizer
        model_filepath = f'personality_app/ml_models/{model_name}_model.joblib'
        tfidf_filepath = 'personality_app/ml_models/tfidf_vectorizer.joblib'
        # scalar_filepath = 'personality_app/ml_models/scalar.joblib'

        self.model = joblib.load(model_filepath)
        self.tfidf_vectorizer = joblib.load(tfidf_filepath)
        # self.scalar = joblib.load(scalar_filepath)

    def predict(self, text):
        # Transform the input text using the loaded TF-IDF vectorizer
        X = self.tfidf_vectorizer.transform([text])
        # Make predictions using the loaded model
        # pred = self.model.predict(X)
        # score = self.scalar.inverse_transform(pred.reshape(-1, 1))[0][0]
        score = self.model.predict(X)[0]
        return score

def result_mapper(data):
    return {key: 'YES' if value == 1 else 'NO' for key, value in data.items()}

def predict_traits(text):
    traits = ['cOPN', 'cCON', 'cEXT', 'cAGR', 'cNEU']

    result = {}
    for trait in traits:
        model = SVMModel(trait)
        pred = model.predict(text)
        result[trait] = pred
        
    return result_mapper(result)

if __name__ == "__main__":
    
    text = "how are you"
    result = predict_traits(text)
    print(result)