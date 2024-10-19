# ActiveRAG: Autonomously Knowledge Assimilation and Accommodation through Retrieval-Augmented Agents

Source code for our paper :  
***[ActiveRAG: Autonomously Knowledge Assimilation and Accommodation through Retrieval-Augmented Agents](https://arxiv.org/abs/2402.13547)***

We are currently optimizing the code and have uploaded the original version.

## Quick Start

1️⃣ Install from git

```bash
git clone https://github.com/OpenMatch/ActiveRAG
cd ActiveRAG
```

2️⃣ Install the necessary packages

```bash
pip install -r requirements.txt
```

3️⃣ Set your own api here.

```python
MODEL = "EMPTY"
openai_api_key = "EMPTY"
openai_api_base = "EMPTY"
```

4️⃣ Run the following script:

```bash
python -m scripts.run --dataset nq --topk 5
```

5️⃣ Analyzing logs:

```bash
python -m scripts.build --dataset nq --topk 5
```

6️⃣ Evaluate:

```bash
python -m scripts.evaluate --dataset nq --topk 5
```

## Citation

```
@article{xu2024activerag,
  title={ActiveRAG: Autonomously Knowledge Assimilation and Accommodation through Retrieval-Augmented Agents},
  author={Xu, Zhipeng and Liu, Zhenghao and Yan, Yukun and Wang, Shuo and Yu, Shi and Zeng, Zheni and Xiao, Chaojun and Liu, Zhiyuan and Yu, Ge and Xiong, Chenyan},
  journal={arXiv preprint arXiv:2402.13547},
  year={2024}
}
```

## Contact Us

If you have questions, suggestions, and bug reports, please send a email to us, we will try our best to help you. 
