from setuptools import find_packages, setup

setup(
    name="pbt_tutorial",
    description="Library code for property-based testing tutorial",
    packages=find_packages(where="src", exclude=["tests*"]),
    package_dir={"": "src"},
    version="1.1.0",
    python_requires=">=3.7",
    install_requires=["numpy>=1.11"],
    tests_requires=["pytest >= 7.1", "hypothesis >= 6.45"],
)
