# Etbaly AI Engine 🚀

A unified, high-performance AI engine for **Text-to-Image** and **Image-to-3D** generation. Optimized for production environments and NVIDIA Tesla T4 (Cloud/Headless) environments.

## 🛠 Features

- **Unified API:** A single Flask server handling both 2D and 3D generation.
- **Turbo Speed:** Integrated with `Hunyuan3D-2.0-Turbo` and distilled `HunyuanDiT` models for near-instant inference.
- **VRAM Optimized:** Specifically tuned for NVIDIA T4 (16GB) GPUs.
- **Headless Ready:** Pre-configured with necessary OpenGL/EGL system libraries.
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

### 1. Clean Workspace & Clone the repository
Since Lightning AI workspaces often contain pre-existing hidden configuration files, use this method to clear the root directory and clone the repo directly without creating a nested folder:
   
```bash
# 0. (Optional) Delete all existing files and directories in the current root
rm -rf ./* ./.* 2>/dev/null

# 1. Clone into a temporary folder
git clone https://github.com/etbalyprints/Etbaly_AI temp_repo

# 2. Move all files (including hidden ones like .git) to the current directory
mv temp_repo/* temp_repo/.* . 2>/dev/null

# 3. Clean up the empty temporary folder
rm -rf temp_repo

# 4. Start the server (handles dependencies and background launch)
bash .lightning_studio/on_start.sh
```

### 2. Automated Provisioning
The server, system dependencies, and Python libraries are automatically managed via `.lightning_studio/on_start.sh`. Simply start or restart your Studio instance. The server will launch in the background. Monitor status via:
```bash
tail -f server_unified.log
```

### 3. Manual Control (Optional)
If you need to restart the server manually:
```bash
python server_api.py
```

## ⚡ Lightning Studio Tips

### Prevent Auto-Stop (Keep Awake)
Lightning AI automatically stops inactive instances after a certain period (e.g., 10-15 minutes). If your server is running in the background via `nohup` and you want to prevent the workspace from sleeping, open a separate terminal and run this keep-alive loop:

```bash
while true; do echo "[$(date)] Keeping Lightning Studio awake... ⚡"; sleep 300; done
```
*(Note: Remember to manually stop your studio when finished to conserve your credits!)*

## 🧪 Testing the API

**Postman**
A pre-configured Postman collection is included: `Etbaly_AI_Collection.postman_collection.json`. Simply import it into Postman to start testing.

### Endpoints

| Method | Endpoint | Description | Payload |
|---|---|---|---|
| **GET** | `/` | Health Check | N/A |
| **POST** | `/generate-image` | Text → Image | `{"prompt": "A modern chair", "seed": 0}` |
| **POST** | `/generate-shape` | Image → 3D (.stl) | `multipart/form-data` with image file |

## ⚙️ Configuration

The engine uses the following high-performance models by default:
- **2D:** `Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled` (12 Steps)
- **3D:** `tencent/Hunyuan3D-2mini-turbo` (6 Steps + FlashVDM)

## 🤝 Contributing

This project is maintained by **Etbaly Prints**. For support or contributions, please contact the AI Engineering team.

*Developed for excellence in 3D AI generation.*
