import csv
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--dataset', required=True)
parser.add_argument('--topk', type=int, required=True)
args = parser.parse_args()

dataset = args.dataset
topk = args.topk

correctness_columns = ['anchoring_correctness', 'associate_correctness', 'logician_correctness', 'cognition_correctness']

def evaluate(file_name):
    with open(file_name, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    for column in correctness_columns:
        column_accuracy = calculate_accuracy(data, column)
        print(f"{file_name} {column} Accuracy: {column_accuracy:.2f}%")

def calculate_accuracy(data, column):
    correctness_values = [row[column] for row in data]
    accuracy = 100 * np.mean([1 if correctness == 'True' else 0 for correctness in correctness_values])
    return accuracy


file_name = f'log/activerag/{dataset}/top{topk}/result.csv'

evaluate(file_name)