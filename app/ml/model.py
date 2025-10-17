from diffusers import DiffusionPipeline
import torch

_pipeline = None


def _load_pipeline():
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
        pipe.enable_attention_slicing()
    else:
        pipe = pipe.to("cpu")
    _pipeline = pipe
    return _pipeline


def generate_image(prompt: str):
    """Generate an image from a text prompt using a cached pipeline."""
    pipeline = _load_pipeline()
    image = pipeline(prompt).images[0]
    return image
