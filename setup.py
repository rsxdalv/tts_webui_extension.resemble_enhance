import setuptools

setuptools.setup(
    name="tts_webui_extension.resemble_enhance",
    packages=setuptools.find_namespace_packages(),
    version="0.1.0",
    author="rsxdalv",
    description="Resemble Enhance Extension",
    license="MIT",
    url="https://github.com/rsxdalv/tts_webui_extension.audio_separator",
    project_urls={},
    scripts=[],
    install_requires=[
        "resemble-enhance @ git+https://github.com/rsxdalv/resemble-enhance@main",
        "numpy < 2",  # gradio breaking
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

