import setuptools

setuptools.setup(
    name="extension_resemble_enhance",
    packages=setuptools.find_namespace_packages(),
    version="0.0.1",
    author="rsxdalv",
    description="Resemble Enhance Extension",
    license="MIT",
    url="https://github.com/rsxdalv/extension_audio_separator",
    project_urls={},
    scripts=[],
    install_requires=[
        "resemble-enhance @ git+https://github.com/resemble-ai/resemble-enhance@d20c3728f39eb9ec1f2950d9742942acc4ac6cb8",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
