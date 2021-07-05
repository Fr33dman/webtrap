import unittest
from app import app


class FlaskTest(unittest.TestCase):

    # Тестим /api GET запросом
    def test_api_get(self):
        tester = app.test_client(self)
        response = tester.get('/api')
        status = response.status_code
        self.assertEqual(status, 200)

    # Тестим /api GET запросом с параметром notawaiting (передал параметр вручную,
    # потому что параметры туда словарем, как в requests не передаются почему-то, может я доку не дочитал)
    def test_api_notawaiting_get(self):
        tester = app.test_client(self)
        response = tester.get('/api?notawaiting=1')
        status = response.status_code
        self.assertEqual(status, 200)

    # Тестим /api POST запросом
    def test_api_post(self):
        tester = app.test_client(self)
        response = tester.post('/api')
        status = response.status_code
        self.assertEqual(status, 200)

    # Тестим какой то endpoint просто GET запросом
    def test_random_endpoint_get(self):
        tester = app.test_client(self)
        response = tester.get('/any_url')
        status = response.status_code
        self.assertEqual(status, 200)

    # Тестим какой то endpoint GET запросом с параметром invalid=1
    def test_random_endpoint_invalid_get(self):
        tester = app.test_client(self)
        response = tester.get('/any_url?invalid=1')
        status = response.status_code
        self.assertEqual(status, 200)

    # Тестим опять же какой то endpoint PUT (любым не GET запросом)
    def test_random_endpoint_put(self):
        tester = app.test_client(self)
        response = tester.put('/any_url')
        status = response.status_code
        self.assertEqual(status, 200)


if __name__ == '__main__':
    unittest.main()
