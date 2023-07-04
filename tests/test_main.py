## To Implement
from src.main import Main
import os
import pytest

def test_token_present():
    os.environ['OXYGENCS_TOKEN'] = 'TEST_TOKEN'
    main = Main()
    assert main.TOKEN == 'TEST_TOKEN'

def test_token_missing():
    del os.environ['OXYGENCS_TOKEN']
    with pytest.raises(Exception) as excinfo:
        main = Main()
    assert "ERREUR: TOKEN MANQUANT DANS LES VARIABLES DENVIRONNEMENT" in str(excinfo)