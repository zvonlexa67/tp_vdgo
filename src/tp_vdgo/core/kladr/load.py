import asyncio
from .kladr import kladr

def load():
    kl = kladr()
    asyncio.run(kl.loadDBF())
