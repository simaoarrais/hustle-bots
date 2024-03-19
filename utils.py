import os

def create_output_folder():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the 'output' folder if it doesn't exist
    output_dir = os.path.join(script_dir, 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)