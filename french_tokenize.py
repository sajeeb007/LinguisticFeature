import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tqdm import tqdm

# Download the necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load the French stopwords
french_stopwords = set(stopwords.words('french'))

# Function to tokenize a given text
def tokenize_french_text(text):
    # Tokenize the text into words and punctuation marks
    tokens = nltk.tokenize.WordPunctTokenizer().tokenize(text)
    
    # Remove stopwords
    filtered_tokens = [token for token in tokens if token.lower() not in french_stopwords]
    
    return filtered_tokens

# Function to tokenize a dataset file
def tokenize_dataset_file(input_file, output_file):
    tokenized_text = []
    
    # Read the file contents
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.readlines()
    
    # Tokenize the text with progress bar
    for line in tqdm(text, desc="Tokenizing", unit="lines"):
        tokenized_line = tokenize_french_text(line)
        tokenized_text.append(' '.join(tokenized_line) + '\n')
    
    # Save the tokenized dataset to a text file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(tokenized_text)
    
    print(f"Tokenized data saved to: {output_file}")

# Example usage
input_file = 'en-fr/train.fr'
output_file = 'en-fr/tokenized.fr'
tokenize_dataset_file(input_file, output_file)
 