import os

directory = os.path.dirname(os.path.abspath(__file__))

__all__ = [os.path.splitext(i)[0] for i in os.listdir(directory) if i.endswith('.py')]
