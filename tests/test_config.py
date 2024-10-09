import unittest
import os
import base64
from skoleintra.config import ProfileConf

class TestProfileConf(unittest.TestCase):
    def setUp(self):
        # Create a temporary configuration file for testing
        self.config_file = 'test_config.txt'
        with open(self.config_file, 'w') as f:
            f.write("[default]\n")
            f.write("username=test_user\n")
            f.write("password=pswd:")
            f.write(base64.b64encode("test_password".encode('utf-8')).decode('utf-8'))
            f.write("\n")

    def tearDown(self):
        # Remove the temporary configuration file after tests
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_read_username_and_password(self):
        profile_conf = ProfileConf('default')
        profile_conf.read(self.config_file)

        # Assert that the username and password are read correctly
        self.assertEqual(profile_conf['username'], 'test_user')
        self.assertEqual(profile_conf.b64dec(profile_conf['password']), 'test_password')

if __name__ == '__main__':
    unittest.main()