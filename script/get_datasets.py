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
        os.makedirs(dataset_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{datasets_name}_{split}.jsonl")
        with open(output_path, "w", encoding="utf-8") as f:
            for example in dataset[split]:
                json.dump(example, f, ensure_ascii=False)
                f.write("\n")
        print(f"✅ Saved {split} split to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--datasets",
        type=str,
        required=True
    )
    args = parser.parse_args()
    datasets_name = args.datasets
    main(datasets_name)
