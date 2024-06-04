
import unittest
from models import *

class TestAjoutClient(unittest.TestCase):
    def test_ajout_objet(self):
        client = self.app.test_client()
        response = client.post('/objet', json={
            "codobj": 1,
            "libobj": "Objet Test",
            "tailleobj": "M",
            "puobj": 12.99,
            "poidsobj": 0.5,
            "indispobj": 1,
            "o_imp": 0,
            "o_aff": 1,
            "o_cartp": 0,
            "points": 100,
            "o_ordre_aff": 1,
        })

        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertEqual(data["codobj"], 1)
        self.assertEqual(data["libobj"], "Objet Test")
        self.assertEqual(data["tailleobj"], "M")
        self.assertEqual(data["puobj"], 12.99)
        self.assertEqual(data["poidsobj"], 0.5)
        self.assertEqual(data["indispobj"], 1)
        self.assertEqual(data["o_imp"], 0)
        self.assertEqual(data["o_aff"], 1)
        self.assertEqual(data["o_cartp"], 0)
        self.assertEqual(data["points"], 100)
        self.assertEqual(data["o_ordre_aff"], 1)

if __name__ == '__main__':
    unittest.main()
    print("TEST OK")