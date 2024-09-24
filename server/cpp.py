import ctypes


def cpp_function(words):
    """
    Calls a C++ function to recognize words and determine if they match a disease.

    Parameters:
    words (list of str): A list of words to be processed by the C++ function.

    Returns:
    tuple: A tuple containing:
        - result (list of str or str): A list of recognized states' names or the name of the disease.
        - is_disease (bool): A flag indicating if a disease was recognized.
    """
    if len(words) == 0:
        return [], False

    # Load the C++ DLL
    try:
        lib = ctypes.CDLL(r'..\dfa2\x64\Debug\dfa2.dll')
    except OSError as e:
        print(f"Error loading DLL: {e}")
        return [], False

    # Define the CState structure to match the C++ struct
    class CState(ctypes.Structure):
        _fields_ = [("id", ctypes.c_int),
                    ("isLast", ctypes.c_bool),
                    ("isDisease", ctypes.c_bool),
                    ("name", ctypes.c_wchar * 100)]

    # Define the argument types and return type for the C++ function
    lib.recognizeWords.argtypes = [ctypes.POINTER(ctypes.c_char_p), ctypes.c_int, ctypes.POINTER(CState)]
    lib.recognizeWords.restype = None

    # Prepare the input for the C++ function
    word_ptrs = [ctypes.c_char_p(word.encode('utf-8')) for word in words]
    word_ptrs.append(None)  # Add a NULL pointer to the end of the list
    max_output_size = len(words)
    output_array = (CState * max_output_size)()  # Create an array of CState structures

    # Call the C++ function
    try:
        lib.recognizeWords((ctypes.c_char_p * len(word_ptrs))(*word_ptrs), max_output_size, output_array)
    except Exception as e:
        print(f"Error during C++ function call: {e}")
        return [], False

    # Process the output from the C++ function
    result = []
    if output_array[0].isDisease:
        return output_array[0].name, True

    for state in output_array:
        if state.name != '':
            result.append(state.name)

    return result, False

