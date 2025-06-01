import gradio as gr
from pathlib import Path

RUN_DIR = Path("./") / "data" / "models" / "resemble_enhance"


def extension__tts_generation_webui():
    resemble_enhance_ui()
    return {
        "package_name": "extension_resemble_enhance",
        "name": "Resemble Enhance",
        "requirements": "git+https://github.com/rsxdalv/extension_resemble_enhance@main",
        "description": "Resemble Enhance allows enhancing audio files.",
        "extension_type": "interface",
        "extension_class": "audio-conversion",
        "author": "rsxdalv",
        "extension_author": "rsxdalv",
        "license": "MIT",
        "website": "https://github.com/rsxdalv/extension_resemble_enhance",
        "extension_website": "https://github.com/rsxdalv/extension_resemble_enhance",
        "extension_platform_version": "0.0.1",
    }


def _denoise_enhance(path, solver, nfe, tau, denoising):
    import torch
    import torchaudio

    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    from resemble_enhance.enhancer.inference import denoise, enhance, download

    if path is None:
        return None, None

    solver = solver.lower()
    nfe = int(nfe)
    lambd = 0.9 if denoising else 0.1

    dwav, sr = torchaudio.load(path)
    dwav = dwav.mean(dim=0)

    download(RUN_DIR, safetensors=True)
    wav1, new_sr = denoise(dwav, sr, device, run_dir=RUN_DIR / "denoiser")
    wav2, new_sr = enhance(
        dwav, sr, device, nfe=nfe, solver=solver, lambd=lambd, tau=tau, run_dir=RUN_DIR / "enhancer", skip_download=True,
    )

    wav1 = wav1.cpu().numpy()
    wav2 = wav2.cpu().numpy()

    return (new_sr, wav1), (new_sr, wav2)


def resemble_enhance_ui():
    gr.Markdown(
        "AI-driven audio enhancement for your audio files, powered by Resemble AI."
    )
    with gr.Row():
        with gr.Column():
            inputs: list = [
                gr.Audio(type="filepath", label="Input Audio"),
                gr.Dropdown(
                    choices=["Midpoint", "RK4", "Euler"],
                    value="Midpoint",
                    label="CFM ODE Solver",
                ),
                gr.Slider(
                    minimum=1,
                    maximum=128,
                    value=64,
                    step=1,
                    label="CFM Number of Function Evaluations",
                ),
                gr.Slider(
                    minimum=0,
                    maximum=1,
                    value=0.5,
                    step=0.01,
                    label="CFM Prior Temperature",
                ),
                gr.Checkbox(value=False, label="Denoise Before Enhancement"),
            ]
            denoise_button = gr.Button("Denoise and Enhance", variant="primary")

        with gr.Column():
            outputs: list = [
                gr.Audio(label="Output Denoised Audio"),
                gr.Audio(label="Output Enhanced Audio"),
            ]

    denoise_button.click(
        fn=_denoise_enhance,
        inputs=inputs,
        outputs=outputs,
    )


if __name__ == "__main__":
    with gr.Blocks() as demo:
        resemble_enhance_ui()

    demo.launch()
    # python -m workspace.extension_resemble_enhance.extension_resemble_enhance.main
