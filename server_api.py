import sys
import os
import torch
import base64
import io
import warnings
import logging
from flask import Flask, request, jsonify, send_file
from PIL import Image

# Suppress specific deprecation warnings from transformers
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
warnings.filterwarnings("ignore", message=".*Siglip2ImageProcessorFast.*")

# Suppress transformers logging
try:
    import transformers
    transformers.utils.logging.set_verbosity_error()
except ImportError:
    pass
logging.getLogger("transformers").setLevel(logging.ERROR)

# Core Imports from local hy3dgen module
try:
    from hy3dgen.shapegen.pipelines import Hunyuan3DDiTFlowMatchingPipeline
    from hy3dgen.text2image import HunyuanDiTPipeline
except ImportError as e:
    print(f"Error importing hy3dgen: {e}")
    sys.exit(1)

app = Flask(__name__)

# Initialize Models
device = "cuda" if torch.cuda.is_available() else "cpu"

# Lazy loading to avoid OOM on startup
t2i_pipe = None
i23d_pipe = None

def get_t2i_pipe():
    global t2i_pipe
    if t2i_pipe is None:
        try:
            # Note: HunyuanDiTPipeline in hy3dgen uses "Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled" by default
            t2i_pipe = HunyuanDiTPipeline(device=device)
            print("Compiling T2I model for speed...")
            t2i_pipe.compile() # Hot start and kernel optimization
        except Exception as e:
            print(f"Error loading T2I pipe: {e}")
            raise e
    return t2i_pipe

def get_i23d_pipe():
    global i23d_pipe
    if i23d_pipe is None:
        try:
            # Using Hunyuan3D-2mini-turbo which is the absolute fastest for T4
            pipe = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
                "tencent/Hunyuan3D-2mini", 
                subfolder="hunyuan3d-dit-v2-mini-turbo",
                torch_dtype=torch.float16
            )
            pipe.to(device)
            print("Enabling FlashVDM Turbo Mode...")
            pipe.enable_flashvdm() # Uses turbo VAE
            # Skipping pipe.compile() to avoid the 10-minute startup/first-run delay
            i23d_pipe = pipe
        except Exception as e:
            print(f"Error loading I23D pipe: {e}")
            raise e
    return i23d_pipe

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "online", "device": str(device)})

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json or {}
    prompt = data.get('prompt', 'A high-tech digital kitchen')
    seed = data.get('seed', 0)
    
    try:
        pipe = get_t2i_pipe()
        with torch.no_grad():
            # Already optimized to 12 steps and 512 res in hy3dgen/text2image.py
            image = pipe(prompt, seed=seed)
        
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()
        
        torch.cuda.empty_cache()
        return jsonify({"image": img_b64, "success": True})
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

import traceback

@app.route('/generate-shape', methods=['POST'])
def generate_shape():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    try:
        # Use .stream for explicit compatibility
        input_image = Image.open(request.files['image'].stream).convert("RGB")
        
        pipe = get_i23d_pipe()
        with torch.no_grad():
            # Speed Optimizations:
            # 1. num_inference_steps=6 (Turbo range)
            # 2. octree_resolution=256 (Lower = much faster)
            # 3. num_chunks=16000 (Faster batching)
            meshes = pipe(
                input_image, 
                num_inference_steps=6, 
                octree_resolution=256,
                num_chunks=16000
            )
            # Handle both list and single mesh returns
            if isinstance(meshes, list):
                mesh = meshes[0]
            else:
                mesh = meshes
        
        # Save to an in-memory buffer instead of disk
        buffered = io.BytesIO()
        mesh.export(buffered, file_type="stl")
        buffered.seek(0)
        
        torch.cuda.empty_cache()
        return send_file(
            buffered, 
            mimetype='application/octet-stream',
            as_attachment=True, 
            download_name='model.stl'
        )
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

if __name__ == '__main__':
    # Pre-load models to download them automatically on first run
    print("Pre-loading models... This may take several minutes on the first run.")
    try:
        get_t2i_pipe()
        get_i23d_pipe()
        print("Models loaded successfully.")
    except Exception as e:
        print(f"Warning: Model pre-loading failed: {e}. They will attempt to load on first request.")
    
    # Increase timeout for heavy model loading
    app.run(host='0.0.0.0', port=8080, threaded=True)
