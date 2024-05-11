# import os
# import shutil

# def split_dataset(input_file_fr, input_file_en, output_dir, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2):
#     # Calculate total number of lines
#     total_lines = sum(1 for line in open(input_file_fr))

#     # Calculate number of lines for train, val, and test
#     train_lines = int(total_lines * train_ratio)
#     val_lines = int(total_lines * val_ratio)
#     test_lines = total_lines - train_lines - val_lines

#     # Create directories for train, val, and test
#     os.makedirs(output_dir, exist_ok=True)
#     train_dir = os.path.join(output_dir, 'train')
#     val_dir = os.path.join(output_dir, 'val')
#     test_dir = os.path.join(output_dir, 'test')
#     os.makedirs(train_dir, exist_ok=True)
#     os.makedirs(val_dir, exist_ok=True)
#     os.makedirs(test_dir, exist_ok=True)

#     # Copy lines to train set
#     copy_lines(input_file_fr, train_dir, 0, train_lines)
#     copy_lines(input_file_en, train_dir, 0, train_lines)

#     # Copy lines to val set
#     copy_lines(input_file_fr, val_dir, train_lines, train_lines + val_lines)
#     copy_lines(input_file_en, val_dir, train_lines, train_lines + val_lines)

#     # Copy lines to test set
#     copy_lines(input_file_fr, test_dir, train_lines + val_lines, total_lines)
#     copy_lines(input_file_en, test_dir, train_lines + val_lines, total_lines)

# def copy_lines(input_file, output_dir, start_line, end_line):
#     with open(input_file, 'r') as infile:
#         lines = infile.readlines()[start_line:end_line]
#         with open(os.path.join(output_dir, os.path.basename(input_file)), 'a') as outfile:
#             outfile.writelines(lines)

# # Example usage:
# split_dataset('pos.fr', 'en-fr/train.en', 'split_dataset_pos')

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

# Example usage:
split_dataset('short/pos_short.fr', 'short/train_short.en', 'split_dataset_pos', seed=42)
