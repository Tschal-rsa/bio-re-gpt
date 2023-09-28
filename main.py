from config import Config, Eval
from dataset import UniDataset
from models import Baseline
from tqdm.autonotebook import tqdm
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GPT for Biomedical RE')
    parser.add_argument('dataset', type=str, help='BB, DrugVar or DrugProt')
    parser.add_argument('--model', type=str, default='gpt-4', help='gpt-4 or gpt-3.5-turbo')
    args = parser.parse_args()

    config = Config()
    config.path = args.dataset
    config.model = args.model

    dataset = UniDataset(config)
    model = Baseline(config)
    total_eval = Eval()
    for sample in tqdm(dataset):
        evaluation = model(sample)
        total_eval += evaluation
    print(total_eval)
