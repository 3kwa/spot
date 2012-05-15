import unittest
import os

import spot

class TestSpot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dotcloud_yaml = spot.Dotcloud.dotcloud_yaml
        spot.Dotcloud.dotcloud_yaml = 'fixtures/dotcloud.yml'


    def test_instantiation_yaml(self):
        dotcloud = spot.Dotcloud()
        self.assertIsInstance(dotcloud.cache, spot.Redis)
        self.assertEqual(dotcloud.cache.port, spot.Redis.port)

    def test_instantiation_json_precedence_over_yaml(self):
        environment_json = spot.Dotcloud.environment_json
        spot.Dotcloud.environment_json = 'fixtures/environment.json'

        dotcloud = spot.Dotcloud()
        self.assertIsInstance(dotcloud.cache, spot.Redis)
        self.assertEqual(dotcloud.cache.port, 28088)

        spot.Dotcloud.environment_json = environment_json


    @classmethod
    def tearDownClass(cls):
        spot.Dotcloud.dotcloud_yaml = cls.dotcloud_yaml

if __name__ == '__main__':
    unittest.main()
