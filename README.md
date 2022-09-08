
This directory is adapted for the paper "Compositional Generalization in Multilingual Semantic Parsing over Wikidata" to generate RIR representations of MCWQ.

The codes are derived from the [Git repo](https://github.com/google-research/language/tree/master/language/compir) for the paper"Unlocking Compositional Generalization in Pre-trained Models Using Intermediate Representations"

The current version of this library contains:
1. Code for reproducing the train,dev and test sets used in the paper for the reversible transformations.
2. Code for evaluating model predictions (based on triples rather than string exact math) against gold programs.

## Intermediate representations

### Data generation

The script `transform/apply_transformation.py` prepares the train, dev and test data for RIR transformation.
Example usage:

```shell
for split in mcd1 mcd2 mcd3 iid; do
   for lang in en he kn zh; do
      echo "generating dataset for $split/$lang"
      python -m transform.apply_transformation \
            --transformation="rir" \
            --dataset="cfq" \
            --split=$split \
            --lang=$lang \
            --train_data_path="datasets/$split/train.$lang.txt" \
            --dev_data_path="datasets/$split/dev.$lang.txt" \
            --test_data_path="datasets/$split/test.$lang.txt" \
            --output_path="datasets/processed"
      done
done
```
For this example, the files from `mcd1_rir_en_train.tsv` to `iid_rir_zh_test.tsv`, which have programs in their reversible intermediate representation, will be created under the `output_path` directory.

Note that `iid` is equivalent to `random_split` refered in the MCWQ paper.

### Evaluation
The script `evaluate/evaluate_predictions.py` evaluates model predictions against the gold test data. For running it, provide a train and test set in the format described above, along with a prediction file and the transformation that was used to create the predictions.
Example usage:

```shell
for split in mcd1 mcd2 mcd3 iid; do
   for lang in en he kn zh; do
      echo "evaluate predictions for $split/$lang"
      python -m evaluate.evaluate_predictions \
           --transformation="rir”\
	   --dataset="cfq" \
	   --train_data_path="datasets/$split/train.$lang.txt" \
	   --dev_data_path="datasets/$split/dev.$lang.txt" \
	   --test_data_path="datasets/$split/test.$lang.txt" \
	   --prediction_path="predictions/$split/rir_predictions_$lang.txt" \
	   --output_path="model/output"
      done
done
```
For this example, the files `predictions/MCD1/rir_predictions_en.txt` holds the predictions for MCWQ MCD1 test set in a reversible intermediate representation.

The reported accuracy is based on whether the triple, prefix and filter sections match.

The predictions in reversed format (from RIR to original SPARQL) will be stored in the directory `model/output`. Note that their orders of the triples and filters might be different from the gold programs, and therefore they should not be used for measuring exact string match directly.