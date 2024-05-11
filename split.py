import argparse
import os
import shutil
import random

def split_dataset(input_file_fr, input_file_en, output_dir, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2, seed=None):
    # Read French and English lines
    with open(input_file_fr, 'r', encoding='utf-8') as f_fr:
        lines_fr = f_fr.readlines()

    with open(input_file_en, 'r', encoding='utf-8') as f_en:
        lines_en = f_en.readlines()

    # Combine French and English lines
    combined_lines = list(zip(lines_fr, lines_en))

    # Shuffle the combined lines with a seed
    if seed is not None:
        random.seed(seed)
    random.shuffle(combined_lines)

    # Calculate total number of lines
    total_lines = len(combined_lines)

    # Calculate number of lines for train, val, and test
    train_lines = int(total_lines * train_ratio)
    val_lines = int(total_lines * val_ratio)
    test_lines = total_lines - train_lines - val_lines

    # Create directories for train, val, and test
    os.makedirs(output_dir, exist_ok=True)
    train_dir = os.path.join(output_dir, 'train')
    val_dir = os.path.join(output_dir, 'val')
    test_dir = os.path.join(output_dir, 'test')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Copy lines to train set
    copy_lines(combined_lines[:train_lines], train_dir)

    # Copy lines to val set
    copy_lines(combined_lines[train_lines:train_lines + val_lines], val_dir)

    # Copy lines to test set
    copy_lines(combined_lines[train_lines + val_lines:], test_dir)

def copy_lines(lines, output_dir):
    with open(os.path.join(output_dir, 'fr.txt'), 'a', encoding='utf-8') as f_fr, \
         open(os.path.join(output_dir, 'en.txt'), 'a', encoding='utf-8') as f_en:
        for line_fr, line_en in lines:
            f_fr.write(line_fr)
            f_en.write(line_en)

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Split dataset into train, val, and test sets")
    parser.add_argument("input_file_fr", type=str, help="Path to the input French file")
    parser.add_argument("input_file_en", type=str, help="Path to the input English file")
    parser.add_argument("output_dir", type=str, help="Path to the output directory")
    parser.add_argument("--train_ratio", type=float, default=0.6, help="Ratio of the dataset to use for training")
    parser.add_argument("--val_ratio", type=float, default=0.2, help="Ratio of the dataset to use for validation")
    parser.add_argument("--test_ratio", type=float, default=0.2, help="Ratio of the dataset to use for testing")
    parser.add_argument("--seed", type=int, default=None, help="Seed for shuffling the dataset")
    args = parser.parse_args()

    # Call the function with provided file paths and arguments
    split_dataset(args.input_file_fr, args.input_file_en, args.output_dir, args.train_ratio, args.val_ratio, args.test_ratio, args.seed)
