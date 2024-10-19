import json
import os
import csv
from argparse import ArgumentParser
from src.metrics import exact_presence

parser = ArgumentParser()
parser.add_argument('--dataset', required=True)
parser.add_argument('--topk', type=int, required=True)
args = parser.parse_args()

dataset = args.dataset
topk = args.topk


def acc(output):
    correctness = exact_presence(answer_key, output)
    return correctness


csv_file_path = f'log/activerag/{dataset}/top{topk}/result.csv'
csv_columns = ['id', 'anchoring_output', 'anchoring_correctness', 'associate_output', 'associate_correctness',
               'logician_output', 'logician_correctness', 'cognition_output', 'cognition_correctness', 'true_answer']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    csv_writer.writeheader()

    for i in range(500):
        file_path = f'log/activerag/{dataset}/top{topk}/{dataset}_idx_{i}.json'

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                answer_key = data["question_info"]["__answers__"]

                anchoring_output = data["anchoring"][-1]["content"]
                anchoring_correctness = acc(anchoring_output)

                associate_output = data["associate"][-1]["content"]
                associate_correctness = acc(associate_output)

                logician_output = data["logician"][-1]["content"]
                logician_correctness = acc(logician_output)

                cognition_output = data["cognition"][-1]["content"]
                cognition_correctness = acc(cognition_output)

                csv_writer.writerow(
                    {'id': i, 'anchoring_output': anchoring_output, 'anchoring_correctness': anchoring_correctness,
                     'associate_output': associate_output, 'associate_correctness': associate_correctness,
                     'logician_output': logician_output, 'logician_correctness': logician_correctness,
                     'cognition_output': cognition_output, 'cognition_correctness': cognition_correctness,
                     'true_answer': answer_key})
        else:
            print(f"File not found: {file_path}")

print("CSV file created successfully.")

# python -m scripts.build --dataset nq --topk 5
