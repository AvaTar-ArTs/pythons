#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/mlabonne/llm-course/blob/main/Quantize_Llama_2_models_using_GGUF_and_llama_cpp.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Quantize Llama 2 models using GGUF and llama.cpp
# > 🗣️ [Large Language Model Course](https://github.com/mlabonne/llm-course)
# 
# ❤️ Created by [@maximelabonne](https://twitter.com/maximelabonne).
# 
# ## Usage
# 
# * `MODEL_ID`: The ID of the model to quantize (e.g., `mlabonne/EvolCodeLlama-7b`).
# * `QUANTIZATION_METHOD`: The quantization method to use.
# 
# ## Quantization methods
# 
# The names of the quantization methods follow the naming convention: "q" + the number of bits + the variant used (detailed below). Here is a list of all the possible quant methods and their corresponding use cases, based on model cards made by [TheBloke](https://huggingface.co/TheBloke/):
# 
# * `q2_k`: Uses Q4_K for the attention.vw and feed_forward.w2 tensors, Q2_K for the other tensors.
# * `q3_k_l`: Uses Q5_K for the attention.wv, attention.wo, and feed_forward.w2 tensors, else Q3_K
# * `q3_k_m`: Uses Q4_K for the attention.wv, attention.wo, and feed_forward.w2 tensors, else Q3_K
# * `q3_k_s`: Uses Q3_K for all tensors
# * `q4_0`: Original quant method, 4-bit.
# * `q4_1`: Higher accuracy than q4_0 but not as high as q5_0. However has quicker inference than q5 models.
# * `q4_k_m`: Uses Q6_K for half of the attention.wv and feed_forward.w2 tensors, else Q4_K
# * `q4_k_s`: Uses Q4_K for all tensors
# * `q5_0`: Higher accuracy, higher resource usage and slower inference.
# * `q5_1`: Even higher accuracy, resource usage and slower inference.
# * `q5_k_m`: Uses Q6_K for half of the attention.wv and feed_forward.w2 tensors, else Q5_K
# * `q5_k_s`:  Uses Q5_K for all tensors
# * `q6_k`: Uses Q8_K for all tensors
# * `q8_0`: Almost indistinguishable from float16. High resource use and slow. Not recommended for most users.
# 
# As a rule of thumb, **I recommend using Q5_K_M** as it preserves most of the model's performance. Alternatively, you can use Q4_K_M if you want to save some memory. In general, K_M versions are better than K_S versions. I cannot recommend Q2_K or Q3_* versions, as they drastically decrease model performance.

# In[ ]:


# Variables
MODEL_ID = "mlabonne/EvolCodeLlama-7b"
QUANTIZATION_METHODS = ["q4_k_m", "q5_k_m"]

# Constants
MODEL_NAME = MODEL_ID.split('/')[-1]

# Install llama.cpp
get_ipython().system('git clone https://github.com/ggerganov/llama.cpp')
get_ipython().system('cd llama.cpp && git pull && make clean && LLAMA_CUBLAS=1 make')
get_ipython().system('pip install -r llama.cpp/requirements.txt')

# Download model
get_ipython().system('git lfs install')
get_ipython().system('git clone https://huggingface.co/{MODEL_ID}')

# Convert to fp16
fp16 = f"{MODEL_NAME}/{MODEL_NAME.lower()}.fp16.bin"
get_ipython().system('python llama.cpp/convert.py {MODEL_NAME} --outtype f16 --outfile {fp16}')

# Quantize the model for each method in the QUANTIZATION_METHODS list
for method in QUANTIZATION_METHODS:
    qtype = f"{MODEL_NAME}/{MODEL_NAME.lower()}.{method.upper()}.gguf"
    get_ipython().system('./llama.cpp/quantize {fp16} {qtype} {method}')


# ## Run inference
# 
# Here is a simple script to run your quantized models. I'm offloading every layer to the GPU (35 for a 7b parameter model) to speed up inference.

# In[ ]:


import os

model_list = [file for file in os.listdir(MODEL_NAME) if "gguf" in file]

prompt = input("Enter your prompt: ")
chosen_method = input("Name of the model (options: " + ", ".join(model_list) + "): ")

# Verify the chosen method is in the list
if chosen_method not in model_list:
    print("Invalid name")
else:
    qtype = f"{MODEL_NAME}/{MODEL_NAME.lower()}.{method.upper()}.gguf"
    get_ipython().system('./llama.cpp/main -m {qtype} -n 128 --color -ngl 35 -p "{prompt}"')


# ## Push to hub
# 
# To push your model to the hub, you'll need to input your Hugging Face token (https://huggingface.co/settings/tokens) in Google Colab's "Secrets" tab. The following code creates a new repo with the "-GGUF" suffix. Don't forget to change the `username` variable.

# In[ ]:


get_ipython().system('pip install -q huggingface_hub')
from huggingface_hub import create_repo, HfApi
from google.colab import userdata

# Defined in the secrets tab in Google Colab
hf_token = userdata.get('huggingface')

api = HfApi()
username = "mlabonne"

# Create empty repo
create_repo(
    repo_id = f"{username}/{MODEL_NAME}-GGUF",
    repo_type="model",
    exist_ok=True,
    token=hf_token
)

# Upload gguf files
api.upload_folder(
    folder_path=MODEL_NAME,
    repo_id=f"{username}/{MODEL_NAME}-GGUF",
    allow_patterns="*.gguf",
    token=hf_token
)

