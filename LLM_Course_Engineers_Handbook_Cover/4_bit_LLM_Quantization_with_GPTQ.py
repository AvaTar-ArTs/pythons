#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/mlabonne/llm-course/blob/main/4_bit_LLM_Quantization_with_GPTQ.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # 4-bit LLM Quantization with GPTQ
# > 🗣️ [Large Language Model Course](https://github.com/mlabonne/llm-course)
# 
# ❤️ Created by [@maximelabonne](https://twitter.com/maximelabonne).
# 
# Companion notebook to execute the code from the following article: https://mlabonne.github.io/blog/4bit_quantization/

# In[ ]:


get_ipython().system('BUILD_CUDA_EXT=0 pip install -q auto-gptq transformers')


# In[ ]:


import random

from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
from datasets import load_dataset
import torch
from transformers import AutoTokenizer


# Define base model and output directory
model_id = "gpt2"
out_dir = model_id + "-GPTQ"


# In[ ]:


# Load quantize config, model and tokenizer
quantize_config = BaseQuantizeConfig(
    bits=4,
    group_size=128,
    damp_percent=0.01,
    desc_act=False,
)
model = AutoGPTQForCausalLM.from_pretrained(model_id, quantize_config)
tokenizer = AutoTokenizer.from_pretrained(model_id)


# In[ ]:


# Load data and tokenize examples
n_samples = 1024
data = load_dataset("allenai/c4", data_files="en/c4-train.00001-of-01024.json.gz", split=f"train[:{n_samples*5}]")
tokenized_data = tokenizer("\n\n".join(data['text']), return_tensors='pt')

# Format tokenized examples
examples_ids = []
for _ in range(n_samples):
    i = random.randint(0, tokenized_data.input_ids.shape[1] - tokenizer.model_max_length - 1)
    j = i + tokenizer.model_max_length
    input_ids = tokenized_data.input_ids[:, i:j]
    attention_mask = torch.ones_like(input_ids)
    examples_ids.append({'input_ids': input_ids, 'attention_mask': attention_mask})


# In[ ]:


get_ipython().run_cell_magic('time', '', '\n# Quantize with GPTQ\nmodel.quantize(\n    examples_ids,\n    batch_size=1,\n    use_triton=True,\n)\n\n# Save model and tokenizer\nmodel.save_quantized(out_dir, use_safetensors=True)\ntokenizer.save_pretrained(out_dir)\n')


# In[ ]:


device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Reload model and tokenizer
model = AutoGPTQForCausalLM.from_quantized(
    out_dir,
    device=device,
    use_triton=True,
    use_safetensors=True,
)
tokenizer = AutoTokenizer.from_pretrained(out_dir)


# In[ ]:


from transformers import pipeline

generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
result = generator("I have a dream", do_sample=True, max_length=50)[0]['generated_text']
print(result)

