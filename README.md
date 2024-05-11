# Thesis on Neural Machine Translation with Linguistic Features on French to English Translation
This repository contains the code and resources for my B.Tech's thesis, which investigates the integration of linguistic features such as part-of-speech (POS) tags, named entity recognition (NER), and lemmatization into machine translation systems. The goal of this research is to improve the quality of translations between French and English by leveraging these linguistic insights.
<br />

## Introduction
Machine translation has made significant strides in recent years, but there are still challenges in producing accurate and coherent translations, especially in specific domains or contexts. This research explores the potential of incorporating linguistic features, such as POS tags, NER, and lemmatization, into the source language (French) to enhance the quality of translations into the target language (English).

The core idea is to enrich the input sentences with additional linguistic information, which can provide valuable context and disambiguate ambiguities that might otherwise lead to translation errors. By integrating these features into the source sentences, the machine translation system can potentially learn better representations and produce more accurate and coherent translations.
<br />

## Repository Structure

This repository contains the following main components:

- `addpos.py`: A script to add POS tags to the source (French) sentences.
- `addner.py`: A script to perform named entity recognition (NER) on the source sentences and annotate them accordingly.
- `split.py`: A utility script to split the dataset into training, validation, and test sets.
- `config_baseline.yaml`: Configuration to build vocab and run the entire training
- `readme.md`: A guide on how to install and set up the [OpenNMT-py](https://opennmt.net/OpenNMT-py/) machine translation toolkit, which is used for training and evaluation in this research.

Additionally, the repository includes the dataset used in this research, which is a subset of the Common Corpus dataset, as well as pre-trained models and other relevant resources.

In the following sections, we will provide more details on how to use these scripts, install the required dependencies, and reproduce the experiments from the thesis.

<br />

## Adding POS Tags

To add POS tags to the source (French) sentences, run the `addpos.py` script:

```
python addpos.py --input_file /path/to/input/file --output_file /path/to/output/file
```

This script will process the input file and generate a new file with POS tags added to each word in the source sentences, separated by the pipe (`|`) symbol. For example:

> Cette|PRON maison|NOUN est|VERB belle|ADJ .

Note that the POS tags are added to make the data compatible with OpenNMT-py's linguistic feature integration.


<br />

## Adding Named Entity Recognition

To perform named entity recognition (NER) on the source sentences and annotate them accordingly, run the `addner.py` script:

```
python addner.py --input_file /path/to/input/file --output_file /path/to/output/file
```

This script will process the input file and generate a new file with named entities annotated in the source sentences, again separated by the pipe (`|`) symbol. For example:

> Cette|O maison|O est|O située|O à|O Paris|B-LOC ,|O la|O capitale|O de|O la|O France|B-LOC .

In this example, the named entities "Paris" and "France" are annotated with the `B-LOC` (Beginning of Location) tag.


<br />

## Splitting the Dataset

To split the dataset into training, validation, and test sets, run the `split.py` script:

```
python split.py --input_file /path/to/input/file --train_output /path/to/train/output --val_output /path/to/val/output --test_output /path/to/test/output
```

This script will split the input file into three separate files for training, validation, and testing, respectively. The `--train_output`, `--val_output`, and `--test_output` arguments specify the output file paths for each set.



<br />

## OpenNMT-py Installation

OpenNMT-py is the machine translation toolkit used for training and evaluation in this research. To install OpenNMT-py, follow these steps:

1. Install the required Python packages:
   
   ```
   pip install OpenNMT-py
   ```
<br />

2.  (Optional) Some advanced features (e.g., working with pretrained models or specific transforms) require extra packages. You can install them by downloading the `requirements.opt.txt` file from the [OpenNMT-py repository](https://github.com/OpenNMT/OpenNMT-py/blob/master/requirements.opt.txt) and running:

       ```
       pip install -r requirements.opt.txt
       ```
<br />
3. After installing OpenNMT-py and the necessary dependencies, you can proceed with training and evaluating your machine translation models using the preprocessed data from the previous steps.
<br />




## Training

### Build Vocabulary

Instead of using individual command-line arguments, we have a configuration file named `config_pos.yaml` that contains all the settings we've used during our training.

To build the vocabulary for the machine translation model, run the following command:

``` 
onmt_build_vocab -config config_pos.yaml -n_sample 10000
```

This command will preprocess the training and validation data, build the source and target vocabularies, and save the preprocessed data based on the settings specified in the `config_pos.yaml` file. The `-n_sample 10000` option specifies that the vocabulary should be built by sampling 10,000 examples from the training data.

<br />

### Train

To train the machine translation model with linguistic features, run the following command:

``` 
onmt_train -config config_pos.yaml -n_features 1 -early_stopping 5 -early_stopping_criteria accuracy
```

- `-config config_pos.yaml`: This specifies the configuration file `config_pos.yaml` that contains the settings for the training process.
- `-n_features 1`: This indicates that we are using one additional linguistic feature (in this case, POS tags) along with the source and target sentences. You can use multiple features sepped by the pipe symbol, in such case, increase the count.
- `-early_stopping 5`: This option enables early stopping, which means the training will stop if the validation metric (in this case, accuracy) does not improve for 5 consecutive validation steps.
- `-early_stopping_criteria accuracy`: This specifies that the early stopping criterion is based on the accuracy metric.

Using the configuration file and these additional options, the training process will incorporate the linguistic features and stop early if the validation accuracy does not improve after a certain number of steps, helping to prevent overfitting.
<br />



### Translation

After the model is trained, you can use it to translate new source sentences with the following command:

``` 
onmt_translate -model config_pos/run/model/_step_1000.pt -src path/to/source/file -output path/to/output/file -gpu 0 -verbose -n_features 1
```

- `-model config_pos/run/model/_step_1000.pt`: This specifies the path to the trained model file (in this case, the model at step 1000).
- `-src path/to/source/file`: This is the path to the source file containing the sentences you want to translate.
- `-output path/to/output/file`: This is the path where the translated output will be written.
- `-gpu 0`: This option specifies which GPU to use for inference (in this case, GPU 0).
- `-verbose`: This option enables verbose output, which can be helpful for debugging or monitoring the translation process.
- `-n_features 1`: This indicates that the source sentences have one additional linguistic feature (POS tags) that needs to be considered during translation.

With this command, you can translate new source sentences using the trained model, incorporating the linguistic features for improved translation quality.
<br />



## Evaluation

For evaluating the translation quality, we employ the widely-used BLEU (Bilingual Evaluation Understudy) metric, which measures the similarity between the machine translation output and reference human translations. We use the `sacrebleu` library to calculate the BLEU score.
<br />


### Installing sacrebleu

To install `sacrebleu`, run the following command:

```
pip install sacrebleu
```
<br />



### Applying sacrebleu

Once you have the reference translations (`ref.detok.txt`) and the machine translation output (`output.detok.txt`), you can calculate the BLEU score using the following command:

```
sacrebleu ref.detok.txt -i output.detok.txt -m bleu -b -w 4
```

- `ref.detok.txt`: This is the file containing the reference (human-translated) sentences.
- `-i output.detok.txt`: This specifies the file containing the machine translation output that you want to evaluate.
- `-m bleu`: This option indicates that you want to calculate the BLEU score.
- `-b`: This option enables the calculation of the BLEU score for the entire corpus (as opposed to individual sentences).
- `-w 4`: This sets the maximum n-gram order to 4 (i.e., the BLEU score will be calculated using n-grams up to 4-grams).

The `sacrebleu` command will output the BLEU score, which ranges from 0 to 100, with higher scores indicating better translation quality and closer similarity to the reference translations.

By evaluating the BLEU score of your machine translation output, you can quantify the impact of incorporating linguistic features and compare the performance of different models or configurations.
