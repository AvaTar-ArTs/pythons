#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/mlabonne/llm-course/blob/main/Fine_tune_LLMs_with_Axolotl.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Fine-tune LLMs with Axolotl
# 
# > 🗣️ [Large Language Model Course](https://github.com/mlabonne/llm-course)
# 
# ❤️ Created by [@maximelabonne](https://twitter.com/maximelabonne), based on [Giorgio](https://github.com/g-i-o-r-g-i-o)'s notebook and Axolotl's [example](https://github.com/OpenAccess-AI-Collective/axolotl/blob/main/examples/colab-notebooks/colab-axolotl-example.ipynb).

# In[ ]:


get_ipython().system('git clone -q https://github.com/OpenAccess-AI-Collective/axolotl')
get_ipython().run_line_magic('cd', 'axolotl')
get_ipython().system('pip install -qqq packaging huggingface_hub --progress-bar off')
get_ipython().system("pip install -qqq -e '.[flash-attn,deepspeed]' --progress-bar off")


# In[5]:


import yaml

new_model = "mlabonne/TinyAlpaca"
yaml_string = """
base_model: TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T
model_type: LlamaForCausalLM
tokenizer_type: LlamaTokenizer
is_llama_derived_model: true

load_in_8bit: false
load_in_4bit: true
strict: false

datasets:
  - path: mhenrichsen/alpaca_2k_test
    type: alpaca
dataset_prepared_path:
val_set_size: 0.05
output_dir: ./qlora-out

adapter: qlora
lora_model_dir:

sequence_len: 1096
sample_packing: true
pad_to_sequence_len: true

lora_r: 32
lora_alpha: 16
lora_dropout: 0.05
lora_target_modules:
lora_target_linear: true
lora_fan_in_fan_out:

wandb_project:
wandb_entity:
wandb_watch:
wandb_name:
wandb_log_model:

mlflow_experiment_name: colab-example

gradient_accumulation_steps: 1
micro_batch_size: 1
num_epochs: 4
max_steps: 20
optimizer: paged_adamw_32bit
lr_scheduler: cosine
learning_rate: 0.0002

train_on_inputs: false
group_by_length: false
bf16: false
fp16: true
tf32: false

gradient_checkpointing: true
early_stopping_patience:
resume_from_checkpoint:
local_rank:
logging_steps: 1
xformers_attention:
flash_attention: false

warmup_steps: 10
evals_per_epoch:
saves_per_epoch:
debug:
deepspeed:
weight_decay: 0.0
fsdp:
fsdp_config:
special_tokens:

"""

# Convert the YAML string to a Python dictionary
yaml_dict = yaml.safe_load(yaml_string)

# Specify your file path
yaml_file = 'config.yaml'

# Write the YAML file
with open(yaml_file, 'w') as file:
    yaml.dump(yaml_dict, file)


# In[6]:


get_ipython().system('accelerate launch -m axolotl.cli.train config.yaml')


# In[10]:


get_ipython().system('python3 -m axolotl.cli.merge_lora config.yaml --lora_model_dir="./qlora-out"')


# In[13]:


from huggingface_hub import HfApi

new_model = "mlabonne/TinyAlpaca"

# HF_TOKEN defined in the secrets tab in Google Colab
api = HfApi()

# Upload merge folder
api.create_repo(
    repo_id=new_model,
    repo_type="model",
    exist_ok=True,
)
api.upload_folder(
    repo_id=new_model,
    folder_path="qlora-out/merged",
)

