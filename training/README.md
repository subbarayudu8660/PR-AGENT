## Training

The fine-tuned model was trained on Kaggle using a T4 GPU.

Dataset: 1205 examples (580 real + 625 synthetic)
Base model: meta-llama/Llama-3.2-1B
Method: QLoRA (r=16, alpha=32)
Epochs: 5
Best eval loss: 1.47

Model published at: https://huggingface.co/subbarayudu1234/pr-review-llama-1b-v2