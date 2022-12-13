import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gec_noise_generator_ko",  # Replace with your own username
    version="0.1.2",
    author="Jugyeong Kim",
    author_email="jugyeongkim911@gmail.com",
    description="Noise Generator for Korean Text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JKJIN1999/gec_noise_generator_ko",
    project_urls={
        "Bug Tracker": "https://github.com/JKJIN1999/gec_noise_generator_ko/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
