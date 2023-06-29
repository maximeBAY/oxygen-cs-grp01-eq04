from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import requests
import json
import time
import os

class Main:
    DEFAULT_HOST = 'http://34.95.34.5'
    DEFAULT_DATABASE_HOST = 'TODO'
    DEFAULT_DATABASE_PORT = 'TODO'
    DEFAULT_T_MAX = 30
    DEFAULT_T_MIN = 15
    DEFAULT_TICKETS = 3

    def __get_token_environnement_varable__(self):
        if 'OXYGENCS_TOKEN' not in os.environ:
            raise Exception(('ERREUR: TOKEN MANQUANT DANS LES VARIABLES DENVIRONNEMENT'))
        else:
            return os.environ['OXYGENCS_TOKEN']

    def __get__environnement_variable__(self, varname, default_value):
        if varname in os.environ:
            return os.environ[varname]
        else:
            return default_value
        

    def __init__(self):
        self._hub_connection = None
        self.TOKEN = self.__get_token_environnement_varable__()
        self.HOST = self.__get__environnement_variable__('OXYGENCS_HOST', self.DEFAULT_HOST)
        self.TICKETS = self.__get__environnement_variable__('OXYGENCS_TICKETS', self.DEFAULT_TICKETS)
        self.T_MAX = self.__get__environnement_variable__('OXYGENCS_T_MAX', self.DEFAULT_T_MAX)
        self.T_MIN = self.__get__environnement_variable__('OXYGENCS_T_MIN', self.DEFAULT_T_MIN)
        self.DATABASE_HOST = self.__get__environnement_variable__('OXYGENCS_DATABASE_HOST', self.DEFAULT_DATABASE_HOST)
        self.DATABASE_PORT = self.__get__environnement_variable__('OXYGENCS_DATABASE_PORT', self.DEFAULT_DATABASE_PORT)
        print(self.TOKEN, self.HOST, self.TICKETS, self.T_MAX, self.T_MIN, self.DATABASE_HOST, self.DATABASE_PORT, flush=True)

    def __del__(self):
        if self._hub_connection != None:
            self._hub_connection.stop()

    def setup(self):
        self.setSensorHub()

    def start(self):
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setSensorHub(self):
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )

        self._hub_connection.on("ReceiveSensorData", self.onSensorDataReceived)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(lambda data: print(f"||| An exception was thrown closed: {data.error}"))

    def onSensorDataReceived(self, data):
        try:
            print(data[0]["date"] + " --> " + data[0]["data"])
            date = data[0]["date"]
            dp = float(data[0]["data"])
            #self.send_temperature_to_fastapi(date, dp)
            self.analyzeDatapoint(date, dp)
        except Exception as err:
            print(err)

    def analyzeDatapoint(self, date, data):
        if float(data) >= float(self.T_MAX):
            self.sendActionToHvac(date, "TurnOnAc", self.TICKETS)
        elif float(data) <= float(self.T_MIN):
            self.sendActionToHvac(date, "TurnOnHeater", self.TICKETS)

    def sendActionToHvac(self, date, action, nbTick):
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{nbTick}")
        details = json.loads(r.text)
        print(details)

    def send_event_to_database(self, timestamp, event):
        try:
            # To implement
            pass
        except requests.exceptions.RequestException as e:
            # To implement
            pass


if __name__ == "__main__":
    main = Main()
    main.start()
