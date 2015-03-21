from distutils.core import setup
from minecraft import __version__

setup(name="minecraft",
      version=".".join(__version__),
      description="Python MineCraft library",
      author="Jeppe Klitgaard",
      author_email="jeppe@dapj.dk",
      packages=["minecraft"]
      )
