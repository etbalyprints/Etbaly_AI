# Etbaly AI Engine 🚀

A unified, high-performance AI engine for **Text-to-Image** and **Image-to-3D** generation. Optimized for production environments and NVIDIA Tesla T4 (Cloud/Headless) environments.

## 🛠 Features

- **Unified API:** A single Flask server handling both 2D and 3D generation.
- **Turbo Speed:** Integrated with `Hunyuan3D-2.0-Turbo` and distilled `HunyuanDiT` models for near-instant inference.
- **VRAM Optimized:** Specifically tuned for NVIDIA T4 (16GB) GPUs.
- **Headless Ready:** pre-configured with necessary OpenGL/EGL system libraries.
- **In-Memory Streaming:** Secure and fast processing; results are streamed directly from RAM without disk I/O.
- **Auto-Provisioning:** Automatic model weight downloading and dependency management on first run.

## 📋 Requirements

### Hardware
- **NVIDIA GPU** (Minimum 8GB VRAM, 16GB recommended for full performance).
- At least 30GB of free disk space for model weights.

### Software
- Ubuntu/Linux (Recommended) or Docker.
- Python 3.10+ (Tested on 3.12).
- CUDA 11.8+ installed.

## 🚀 Quick Start (Automated Setup)

This repository is configured to handle its own lifecycle within **Lightning AI Studios**.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/etbalyprints/Etbaly_AI.git
   cd Etbaly_AI
   ```

2. **Automated Provisioning:**
   The server, system dependencies, and Python libraries are automatically managed via `.lightning_studio/on_start.sh`. 
   - Simply start or restart your Studio instance.
   - The server will launch in the background.
   - Monitor status via `tail -f server_unified.log`.

3. **Manual Control (Optional):**
   If you need to restart the server manually:
   ```bash
   python server_api.py
   ```

## 🧪 Testing the API

### Postman
A pre-configured Postman collection is included: `Etbaly_AI_Collection.postman_collection.json`. Simply import it into Postman to start testing.

### Endpoints

| Method | Endpoint | Description | Payload |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Health Check | N/A |
| `POST` | `/generate-image` | Text → Image | `{"prompt": "A modern chair", "seed": 0}` |
| `POST` | `/generate-shape` | Image → 3D (.stl) | `multipart/form-data` with `image` file |

## ⚙️ Configuration

The engine uses the following high-performance models by default:
- **2D:** `Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled` (12 Steps)
- **3D:** `tencent/Hunyuan3D-2mini-turbo` (6 Steps + FlashVDM)

## 🤝 Contributing

This project is maintained by **Etbaly Prints**. For support or contributions, please contact the AI Engineering team.

---
*Developed for excellence in 3D AI generation.*
