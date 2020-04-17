from setuptools import setup

install_requires = [
    # "gurobipy",  	# install this manually
    # "alib",      	# install this manually
    # "vnep_approx" , 	# install this manually
    "matplotlib>=2.2,<2.3",
    "numpy",
    "click==6.7",
    "pyyaml",
    "jsonpickle",
]

setup(
    name="evaluation-ifip-networking-2020",
    packages=["evaluation_ifip_networking_2020"],
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "evaluation-ifip-networking-2020 = evaluation_ifip_networking_2020.cli:cli",
        ]
    }
)