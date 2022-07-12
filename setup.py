from setuptools import setup


setup(
    name='formful',
    install_requires = [
        'markup',
    ],
    extras_require={
        'test': [
            'pytest',
        ]
    }
)
