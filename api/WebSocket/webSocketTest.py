from unittest.mock import patch
from unittest import TestCase

class TestServerResource(TestCase):
    @patch('Websocket.getRoom')
    def test_pagination(self, mock):
    mock.return_value = "poggeris"
    res = self.client().get('/getRoom"')
    print(res)
    self.assertEqual(res.status_code, 200)