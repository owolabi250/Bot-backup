import unittest
import models
from redis import Redis
from unittest.mock import patch, Mock
from models import storage


class TestCache(unittest.TestCase):

    def setUp(self):
        self.cache = storage

    def tearDown(self):
        self.cache.delete('test_key')

    @patch.object(Redis, 'get')
    def test_get_cache_with_cache(self, mock_get):
        mock_get.return_value = None
        result1 = self.cache.get_cache('test_key')
        result2 = self.cache.get_cache('test_key')
        mock_get.assert_called_with('test_key')
        assert result1 == result2 == b'test_value'

    #@patch.object(Redis, 'get')
    def test_get_cache_without_cache(self, mock_get):
        mock_get.return_value = None
        #with patch.object(Redis, 'set') as mock_set:
        result1 = self.cache.get_cache('test_key')
        result2 = self.cache.get_cache('test_key')
        mock_get.assert_called_with('test_key')
        assert result1 == result2 == b'test_value'


    @patch.object(Redis, 'set')
    def test_set_cache(self, mock_set):
        mock_set.return_value = None
        result1 = self.cache.set('test_key', 'test_value')
        result2 = self.cache.set('test_key', 'test_value')
        mock_set.assert_called_with('test_key', 'test_value')
        assert result1 == result2 == True
        #mock_set.assert_called_once_with('test_key', 'test_value')

    def test_delete_cache(self):
        with patch.object(Redis, 'delete') as mock_delete:
            mock_delete.return_value = True
            result = self.cache.delete('test_key')
            self.assertTrue(result)
            mock_delete.assert_called_once_with('test_key')

    def test_exists_cache(self):
        with patch.object(Redis, 'exists') as mock_exists:
            mock_exists.return_value = True
            result = self.cache.exists('test_key')
            self.assertTrue(result)
            mock_exists.assert_called_once_with('test_key')

if __name__ == '__main__':
    unittest.main()
