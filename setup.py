import setuptools

def read(file):
    with open(file) as f:
        content = f.read()
    return content

setuptools.setup(
    name='flagr',
    version='1.0.0',
    description='Use whatever flag you want and stop whining about',
    url='https://github.com/ranisalt/flagr',
    author='Ranieri Althoff',
    author_email='ranisalt+flagr@gmail.com',
    license='MIT',
    install_requires=read('requirements.txt'),
)
