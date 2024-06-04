
import unittest
import models

class TestAjoutClient(unittest.TestCase):
    def test_client_ajoute(self):
        nouveau_client = ajout_client(codcli,genrecli,nomcli,prenomcli,adresse1cli,adresse2cli,adresse3cli,villecli_id,telcli,emailcli,portcli,newsletter)
        