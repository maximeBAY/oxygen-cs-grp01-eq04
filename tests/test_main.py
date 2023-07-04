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

def test_variables_par_defaut():
    del os.environ['OXYGENCS_HOST']
    del os.environ['OXYGENCS_TICKETS']
    del os.environ['OXYGENCS_T_MAX']
    del os.environ['OXYGENCS_T_MIN']
    del os.environ['OXYGENCS_DATABASE']
    del os.environ['OXYGENCS_DATABASE_HOST']
    del os.environ['OXYGENCS_DATABASE_PORT']
    del os.environ['OXYGENCS_DATABASE_USERNAME']
    del os.environ['OXYGENCS_DATABASE_PASSWORD']
    main = Main()
    assert main.HOST == main.DEFAULT_HOST
    assert main.TICKETS == main.DEFAULT_TICKETS
    assert main.T_MAX == main.DEFAULT_T_MAX
    assert main.T_MIN == main.DEFAULT_T_MIN
    assert main.DATABASE == main.DEFAULT_OXYGENCS_DATABASE
    assert main.DATABASE_HOST == main.DEFAULT_DATABASE_HOST
    assert main.DATABASE_PORT == main.DEFAULT_DATABASE_PORT
    assert main.DATABASE_USERNAME == main.DEFAULT_OXYGENCS_DATABASE_USERNAME
    assert main.DATABASE_PASSWORD == main.DEFAULT_OXYGENCS_DATABASE_PASSWORD

def test_variables_environnement():
    main = Main()
    assert main.HOST == os.environ['OXYGENCS_HOST']
    assert main.TICKETS == os.environ['OXYGENCS_TICKETS']
    assert main.T_MAX == os.environ['OXYGENCS_T_MAX']
    assert main.T_MIN == os.environ['OXYGENCS_T_MIN']
    assert main.DATABASE == os.environ['OXYGENCS_DATABASE']
    assert main.DATABASE_HOST == os.environ['OXYGENCS_DATABASE_HOST']
    assert main.DATABASE_PORT == os.environ['OXYGENCS_DATABASE_PORT']
    assert main.DATABASE_USERNAME == os.environ['OXYGENCS_DATABASE_USERNAME']
    assert main.DATABASE_PASSWORD == os.environ['OXYGENCS_DATABASE_PASSWORD']
