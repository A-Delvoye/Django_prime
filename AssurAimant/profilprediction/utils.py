import cloudpickle

def load_model(file_path):
    """
    Chargement du modèle
    """
    with open(file_path, 'rb') as f:
        model = cloudpickle.load(f)
    return model