import pickle


def save_object(
    obj: object,
    file_name: str,
    file_extension: str = '.pickle',
):
    file_path = file_name + file_extension
    with open(file_path, 'wb') as f:
        pickle.dump(
            obj=obj,
            file=f,
            protocol=pickle.HIGHEST_PROTOCOL,
        )


def load_object(
    file_name: str,
    file_extension: str = '.pickle',
) -> object:
    file_path = file_name + file_extension
    with open(file_path, 'rb') as f:
        obj = pickle.load(file=f)

    return obj
