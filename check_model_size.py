import torch
from transformers import AutoModel

# 1. Load your fine-tuned model from the saved directory
# This is the key change: we load your specific model instead of a generic one.
model_path = "model/saved_model"
model = AutoModel.from_pretrained(model_path)

# 2. The rest of your calculation logic remains the same
param_size = 0
buffer_size = 0

for param in model.parameters():
    param_size += param.nelement() * param.element_size()

for buffer in model.buffers():
    buffer_size += buffer.nelement() * buffer.element_size()

size_all_mb = (param_size + buffer_size) / 1024**2

print('Model size: {:.3f} MB'.format(size_all_mb))

