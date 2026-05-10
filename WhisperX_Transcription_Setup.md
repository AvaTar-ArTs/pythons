Here is the translated and formatted English version of your text:

---

# **WhisperX-Based Audio Transcription Tool**  
A transcription tool based on **WhisperX**, offering more flexible configuration options and batch processing capabilities.

## **Features**

### **Core Functions of WhisperX**  
- **Automatic VAD (Voice Activity Detection)** – Detects and segments speech.  
- **Large-Scale Speech Recognition** using Whisper.  
- **Forced Alignment** – Phoneme-level synchronization.  
- **Speaker Diarization** – Identifies and separates different speakers.

### **Enhanced Features**  
- **Comprehensive Configuration System**  
  - Model parameter settings  
  - Input and output configuration  
  - Feature module toggles  
- **Batch File Processing**  
  - Supports multiple audio formats  
  - Allows file-specific processing  
  - Directory-level batch processing  
  - Multi-format output: JSON, SRT, TXT  
- **Memory Management Optimization**

---

## **Installation & Usage**  

### **Setting Up the Python Environment**  
```bash
conda create --name whisperx python=3.10
conda activate whisperx
```

### **Installing PyTorch**  

For **Linux & Windows with CUDA 11.8** (GPU support):  
```bash
conda install pytorch==2.0.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia
```

For **CPU-only installation**:  
```bash
conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 cpuonly -c pytorch
```

### **Installing WhisperX and Dependencies**  
For CPU-only compatibility:  
```bash
pip install -r requirements.txt
```

### **Configuration**  
Modify the `config.yaml` and `secrets.yaml` files.  

In `secrets.yaml`, set the **token** and **proxy** for speaker diarization:  
```yaml
auth_token: "your_token"
proxy: "your_proxy"
```

### **Accepting Model Usage Terms on Hugging Face**  
To use the required models, manually accept the usage terms on Hugging Face:

1. Visit the following pages:  
   - [Segmentation Model](https://huggingface.co/pyannote/segmentation-3.0)  
   - [Speaker Diarization Model](https://huggingface.co/pyannote/speaker-diarization-3.0)  
2. Log in to your **Hugging Face** account (the same account linked to your token).  
3. Click **"Accept"** or **"Access Repository"** to agree to the usage terms.

---

## **Running the Program**  

Use the following command:  
```bash
python WhisperXTranscriber.py
```
Alternatively, you can use the shortcut `"WhisperXConda.lnk"`, but you may need to modify its properties based on the project location.

---

## **Reference**  
GitHub Repository: [Whisper Transcriber](https://github.com/VimWei/WhisperTranscriber)

---

Would you like any additional refinements or clarifications? 🚀