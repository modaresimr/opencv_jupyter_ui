import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opencv_jupyter_ui",
    version="1.4.2",
    author="Seyed Modaresi",
    author_email="alim1369@gmail.com",
    description="A simple widget to display opencv imshow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/modaresimr/opencv_jupyter_ui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'ipycanvas','jupyter-ui-poll','ipywidgets','numpy'
      ],
)