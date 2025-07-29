import argparse

from datasets import load_dataset
import json
import os


def main(datasets_name: str):
    # 当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 父目录
    root_dir = os.path.dirname(current_dir)

    # 加载 Hugging Face 上的 SWE-Gym 数据集
    dataset = load_dataset(datasets_name)

    # 保存目录
    output_dir = os.path.join(root_dir, "datasets")
    os.makedirs(output_dir, exist_ok=True)

    # 将每个 split 保存为 .jsonl
    for split in dataset.keys():
        dataset_dir = os.path.join(output_dir, datasets_name.split("/")[0])
        dataset_file_name = datasets_name.split("/")[-1]
        # 确保目录存在
        os.makedirs(dataset_dir, exist_ok=True)
        output_path = os.path.join(dataset_dir, f"selected_{dataset_file_name}_{split}.jsonl")

        repo_num_dict = {}

        total_number = 0

        with open(output_path, "w", encoding="utf-8") as f:
            for example in dataset[split]:
                # 限制总样本数量为 100
                if total_number >= 100:
                    break

                # 限制每个 repo 的样本数量为 10
                repo = example["repo"]
                if repo not in repo_num_dict:
                    repo_num_dict[repo] = 0
                elif repo_num_dict[repo] < 10:
                    repo_num_dict[repo] += 1
                else:
                    continue

                json.dump(example, f, ensure_ascii=False)
                f.write("\n")
                total_number += 1
        print(f"✅ Saved {split} split to {output_path}")
        print(f"Total number of samples saved: {total_number}")
        print(f"Number of samples per repo: {repo_num_dict}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--datasets",
        type=str,
        required=True,
        default="SWE-Gym/SWE-Gym",
    )
    args = parser.parse_args()
    datasets_name = args.datasets
    main(datasets_name)
