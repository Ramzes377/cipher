from src.api.loader import BinaryLoader


class TestLoaders:
    def test_binary_loader(self):
        r = BinaryLoader.load('./tests/data/testfile')
        assert isinstance(r, bytes)
