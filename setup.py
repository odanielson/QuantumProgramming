from setuptools import setup

setup(
    name="Quantum Programming",
    version="0.1",
    description="Quantum Programming Simulator",
    packages=["qp"],
    entry_points={"console_scripts": ["qrun=qp.qrun:main"]},
)
