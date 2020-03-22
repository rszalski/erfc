import setuptools

setuptools.setup(
    name="erfc",
    version="0.1.0",
    author="Radosław Szalski",
    description='eRFC downloads and formats plain-text RFCs to fit eReaders nicely',
    url='https://github.com/rszalski/erfc',
    download_url='https://github.com/rszalski/erfc/tarball/v0.1.0',
    packages=setuptools.find_packages(),
    keywords=['rfc', 'erfc', 'ebook'],
    install_requires=[
        'docopt>=0.6.1',
        'requests>=2.20.1',
    ],
    entry_points=dict(
        console_scripts=[
            'erfc = erfc:main',
        ]
    )
)
