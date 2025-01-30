import cloudpickle

def load_model(file_path):
    """load_model
    
    Args:
        file_path (string_path): a file path to a saved model

    Returns:
        model:  a genarated model
    """
    with open(file_path, 'rb') as f:
        model = cloudpickle.load(f)
    return model