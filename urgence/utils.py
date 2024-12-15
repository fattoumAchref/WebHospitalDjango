from transformers import pipeline

# Charger le modèle et le tokenizer
classifier = pipeline("text-classification", model="./urgence/model", tokenizer="./urgence/model")

# Mapper les labels aux priorités
label_map = {
    "LABEL_0": "High",
    "LABEL_1": "Medium",
    "LABEL_2": "Low"
}

def predict_priority(description):
    """Retourne la priorité prédite en fonction de la description."""
    if not description:
        return "Inconnu"
    prediction = classifier(description)
    return label_map[prediction[0]["label"]]