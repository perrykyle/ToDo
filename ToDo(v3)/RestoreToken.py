import os
import dotenv
import ast


def get_token_as_dict():
    # Load .env file
    dotenv.load_dotenv()

    # Get the TOKEN string from the environment variables
    token_str = os.getenv('TOKEN')

    # Convert the string representation into a dictionary
    token_dict = ast.literal_eval(token_str)

    return token_dict

