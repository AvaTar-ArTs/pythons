#!/usr/bin/env python
# coding: utf-8
"""
Summary of Mergekit.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""


# <a href="https://colab.research.google.com/github/mlabonne/llm-course/blob/main/Mergekit.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Merge Large Language Models with mergekit
# > 🗣️ [Large Language Model Course](https://github.com/mlabonne/llm-course)
#
# ❤️ Created by [@maximelabonne](https://twitter.com/maximelabonne).
#
# Model merging only requires a lot of RAM. With a free Google Colab account, you should be able to run it using a T4 GPU (VRAM offloading).
#
# Examples of merge configurations:
#
# ### TIES-Merging
#
# ```yaml
# models:
#   - model: mistralai/Mistral-7B-v0.1
#     # no parameters necessary for base model
#   - model: OpenPipe/mistral-ft-optimized-1218
#     parameters:
#       density: 0.5
#       weight: 0.5
#   - model: mlabonne/NeuralHermes-2.5-Mistral-7B
#     parameters:
#       density: 0.5
#       weight: 0.3
# merge_method: ties
# base_model: mistralai/Mistral-7B-v0.1
# parameters:
#   normalize: true
# dtype: float16
# ```
#
# You can find the final model on the Hugging Face Hub at [mlabonne/NeuralPipe-7B-ties](https://huggingface.co/mlabonne/NeuralPipe-7B-ties).
#
# ### SLERP
#
# ```yaml
# slices:
#   - sources:
#       - model: OpenPipe/mistral-ft-optimized-1218
#         layer_range: [0, 32]
#       - model: mlabonne/NeuralHermes-2.5-Mistral-7B
#         layer_range: [0, 32]
# merge_method: slerp
# base_model: OpenPipe/mistral-ft-optimized-1218
# parameters:
#   t:
#     - filter: self_attn
#       value: [0, 0.5, 0.3, 0.7, 1]
#     - filter: mlp
#       value: [1, 0.5, 0.7, 0.3, 0]
#     - value: 0.5
# dtype: bfloat16
# ```
#
# You can find the final model on the Hugging Face Hub at [mlabonne/NeuralPipe-7B-slerp](https://huggingface.co/mlabonne/NeuralPipe-7B-slerp).
#
# ### Passthrough
#
# ```yaml
# slices:
#   - sources:
#     - model: OpenPipe/mistral-ft-optimized-1218
#       layer_range: [0, 32]
#   - sources:
#     - model: mlabonne/NeuralHermes-2.5-Mistral-7B
#       layer_range: [24, 32]
# merge_method: passthrough
# dtype: bfloat16
# ```
#
# You can find the final model on the Hugging Face Hub at [mlabonne/NeuralPipe-9B-merged](https://huggingface.co/mlabonne/NeuralPipe-9B-merged).

# In[ ]:


get_ipython().system("git clone https://github.com/cg123/mergekit.git")
get_ipython().system("cd mergekit && pip install -q -e .")


# In[ ]:


import yaml

MODEL_NAME = "Marcoro14-7B-slerp"
yaml_config = """
slices:
  - sources:
      - model: AIDC-ai-business/Marcoroni-7B-v3
        layer_range: [0, 32]
      - model: EmbeddedLLM/Mistral-7B-Merge-14-v0.1
        layer_range: [0, 32]
merge_method: slerp
base_model: AIDC-ai-business/Marcoroni-7B-v3
parameters:
  t:
    - filter: self_attn
      value: [0, 0.5, 0.3, 0.7, 1]
    - filter: mlp
      value: [1, 0.5, 0.7, 0.3, 0]
    - value: 0.5
dtype: bfloat16

"""

# Save config as yaml file
with open("config.yaml", "w", encoding="utf-8") as f:
    f.write(yaml_config)


# In[ ]:


# Merge models
get_ipython().system(
    "mergekit-yaml config.yaml merge --copy-tokenizer --allow-crimes --out-shard-size 1B --lazy-unpickle"
)


# In[ ]:


get_ipython().system("pip install -qU huggingface_hub")

from huggingface_hub import ModelCard
from jinja2 import Template

username = "mlabonne"

template_text = """
---
license: apache-2.0
tags:
- merge
- mergekit
- lazymergekit
{%- for model in models %}
- {{ model }}
{%- endfor %}
---

# {{ model_name }}

{{ model_name }} is a merge of the following models using [mergekit](https://github.com/cg123/mergekit):

{%- for model in models %}
* [{{ model }}](https://huggingface.co/{{ model }})
{%- endfor %}

## 🧩 Configuration

```yaml
{{- yaml_config -}}
```
"""

# Create a Jinja template object
jinja_template = Template(template_text.strip())

# Get list of models from config
data = yaml.safe_load(yaml_config)
if "models" in data:
    models = [
        data["models"][i]["model"]
        for i in range(len(data["models"]))
        if "parameters" in data["models"][i]
    ]
elif "parameters" in data:
    models = [
        data["slices"][0]["sources"][i]["model"]
        for i in range(len(data["slices"][0]["sources"]))
    ]
elif "slices" in data:
    models = [
        data["slices"][i]["sources"][0]["model"] for i in range(len(data["slices"]))
    ]
else:
    raise Exception("No models or slices found in yaml config")

# Fill the template
content = jinja_template.render(
    model_name=MODEL_NAME,
    models=models,
    yaml_config=yaml_config,
    username=username,
)

# Save the model card
card = ModelCard(content)
card.save("merge/README.md")


# In[ ]:


from google.colab import userdata
from huggingface_hub import HfApi

username = "mlabonne"

# Defined in the secrets tab in Google Colab
api = HfApi(token=userdata.get("HF_TOKEN"))

api.create_repo(repo_id=f"{username}/{MODEL_NAME}", repo_type="model")
api.upload_folder(
    repo_id=f"{username}/{MODEL_NAME}",
    folder_path="merge",
)
