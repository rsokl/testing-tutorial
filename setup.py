from setuptools import find_packages, setup

setup(
    name="pbt_tutorial",
    description="Library code for property-based testing tutorial",
    packages=find_packages(where="src", exclude=["tests*"]),
    package_dir={"": "src"},
    version="1.0.0-solutions",
    python_requires=">=3.6",
    install_requires=["numpy>=1.11"],
    tests_requires=["pytest >= 3.8", "hypothesis >= 4.53.2"],
)
