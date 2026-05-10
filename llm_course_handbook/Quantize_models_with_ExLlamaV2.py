#!/usr/bin/env python
# coding: utf-8
"""
Summary of Quantize_models_with_ExLlamaV2.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""


# <a href="https://colab.research.google.com/github/mlabonne/llm-course/blob/main/Quantize_models_with_ExLlamaV2.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # ExLlamaV2: The Fastest Library to Run LLMs
#
# ❤️ Created by [@maximelabonne](https://twitter.com/maximelabonne) as part of the 🗣️ [Large Language Model Course](https://github.com/mlabonne/llm-course).

# In[ ]:


# Install ExLLamaV2
get_ipython().system("git clone https://github.com/turboderp/exllamav2")
get_ipython().system("pip install -e exllamav2")


# In[ ]:


MODEL_NAME = "zephyr-7b-beta"
BPW = 5.0

# Download model
get_ipython().system("git lfs install")
get_ipython().system("git clone https://huggingface.co/HuggingFaceH4/{MODEL_NAME}")
get_ipython().system("mv {MODEL_NAME} base_model")
get_ipython().system("rm base_mode/*.bin")

# Download dataset
get_ipython().system(
    "wget https://huggingface.co/datasets/wikitext/resolve/9a9e482b5987f9d25b3a9b2883fc6cc9fd8071b3/wikitext-103-v1/wikitext-test.parquet"
)


# In[ ]:


# Quantize model
get_ipython().system("mkdir quant")
get_ipython().system(
    "python exllamav2/convert.py      -i base_model      -o quant      -c wikitext-test.parquet      -b {BPW}"
)


# In[ ]:


# Copy files
get_ipython().system("rm -rf quant/out_tensor")
get_ipython().system(
    "rsync -av --exclude='*.safetensors' --exclude='.*' ./base_model/ ./quant/"
)


# In[ ]:


# Run model
get_ipython().system('python exllamav2/test_inference.py -m quant/ -p "I have a dream"')


# In[ ]:


get_ipython().system("pip install -q huggingface_hub")
get_ipython().system("git config --global credential.helper store")

from huggingface_hub import notebook_login
from huggingface_hub import HfApi
import locale

locale.getpreferredencoding = lambda: "UTF-8"

notebook_login()
api = HfApi()


# In[ ]:


api.create_repo(repo_id=f"mlabonne/{MODEL_NAME}-{BPW:.1f}bpw-exl2", repo_type="model")
api.upload_folder(
    repo_id=f"mlabonne/{MODEL_NAME}-{BPW:.1f}bpw-exl2",
    folder_path="quant",
)
