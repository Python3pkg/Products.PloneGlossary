from setuptools import setup, find_packages

version = '2.0.dev0'
long_description = open("README.rst").read() + "\n\n"
long_description += open("CHANGES.rst").read()
long_description = long_description.decode('utf8')

setup(
    name='Products.PloneGlossary',
    version=version,
    long_description=long_description,
    description="Highlight Plone content terms, mouseover shows the "
                "term definition as tooltip.",
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='plone glossary',
    author='Ingeniweb',
    author_email='support@ingeniweb.com',
    url='https://github.com/collective/Products.PloneGlossary',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'wicked',
    ],
    extras_require={
        'test': ['Products.PloneTestCase'],
    },
)
