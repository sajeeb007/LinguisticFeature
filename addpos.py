import spacy
from tqdm import tqdm

# Load the French language model for spaCy
nlp = spacy.load("fr_core_news_sm")

# Increase the max_length limit
nlp.max_length = 2000000  # Set it to a higher value as per your requirement

def extract_pos_and_append(input_file, output_file):
    # Open the input file for reading and the output file for writing
    with open(input_file, 'r', encoding='utf-8') as f_input, open(output_file, 'w', encoding='utf-8') as f_output:
        # Process each line in the input file
        for line in tqdm(f_input, desc="Processing"):
            # Process the text of the current line using spaCy
            doc = nlp(line)

            # Initialize an empty string to hold the modified text for this line
            modified_text = ""

            # Iterate through each token in the processed text
            for token in doc:
                # Append the token text with its POS tag, skip spaces and newline characters
                if token.text.strip():
                    modified_text += token.text + "|" + token.pos_ + " "

            # Write the modified text with POS tags appended to the output file
            f_output.write(modified_text.rstrip() + '\n')

# Example usage:
source_path = "en-fr/tokenized.fr"  # Path to the input file
save_path = "pos.fr"   # Path to save the modified file

extract_pos_and_append(source_path, save_path)
