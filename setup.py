from setuptools import setup


setup(
    name='formful',
    install_requires = [
        'markup',
        'markupsafe',
    ],
    extras_require={
        'test': [
            'pytest',
        ]
    }
)
