from setuptools import setup, find_packages

setup(
    name="pulsebot",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "ccxt>=4.0.0",
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "flask>=2.0.0",
        "sqlalchemy>=1.4.0",
        "cryptography>=3.4.0",
        "websockets>=10.0",
        "plotly>=5.0.0",
    ],
    include_package_data=True,
    description='PulseBot automated trading framework',
    author='PulseBot contributors',
)
