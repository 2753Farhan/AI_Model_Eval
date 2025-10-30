import os
import json
import gzip
from git import Repo
from tqdm import tqdm

class HumanEvalLoader:
    def __init__(self, repo_url, data_dir):
        self.repo_url = repo_url
        self.data_dir = data_dir
        self.dataset_path = os.path.join(data_dir, "data", "HumanEval.jsonl.gz")

    def fetch_repo(self):
        """Clones the HumanEval repo if not already present."""
        if not os.path.exists(os.path.join(self.data_dir, ".git")):
            print("📥 Cloning HumanEval repository...")
            Repo.clone_from(self.repo_url, self.data_dir)
        else:
            print("✅ Repository already exists. Skipping clone.")

    def load_dataset(self):
        """Loads the dataset into memory as a list of dicts."""
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")

        print("📂 Loading HumanEval dataset...")
        samples = []

        with gzip.open(self.dataset_path, "rt", encoding="utf-8") as f:
            for line in tqdm(f, desc="Reading HumanEval.jsonl.gz"):
                samples.append(json.loads(line))

        print(f"✅ Loaded {len(samples)} problems from HumanEval.")
        return samples
