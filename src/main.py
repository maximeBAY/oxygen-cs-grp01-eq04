from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import requests
import psycopg2
import json
import time
import os

class Main:

    DEFAULT_HOST = 'http://34.95.34.5'
    DEFAULT_TICKETS = 3
    DEFAULT_T_MAX = 30
    DEFAULT_T_MIN = 15
    DEFAULT_DATABASE_HOST = 'postgres'
    DEFAULT_DATABASE_PORT =  5432
    DEFAULT_OXYGENCS_DATABASE="postgres"
    DEFAULT_OXYGENCS_DATABASE_USERNAME="postgres"
    DEFAULT_OXYGENCS_DATABASE_PASSWORD="postgres"
    
    

    def __get_token_environnement_varable__(self):
        if 'OXYGENCS_TOKEN' not in os.environ:
            raise Exception('ERREUR: TOKEN MANQUANT DANS LES VARIABLES DENVIRONNEMENT')
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
        self.DATABASE = self.__get__environnement_variable__('OXYGENCS_DATABASE', self.DEFAULT_OXYGENCS_DATABASE)
        self.DATABASE_HOST = self.__get__environnement_variable__('OXYGENCS_DATABASE_HOST', self.DEFAULT_DATABASE_HOST)
        self.DATABASE_PORT = self.__get__environnement_variable__('OXYGENCS_DATABASE_PORT', self.DEFAULT_DATABASE_PORT)
        self.DATABASE_USERNAME = self.__get__environnement_variable__('OXYGENCS_DATABASE_USERNAME', self.DEFAULT_OXYGENCS_DATABASE_USERNAME)
        self.DATABASE_PASSWORD = self.__get__environnement_variable__('OXYGENCS_DATABASE_PASSWORD', self.DEFAULT_OXYGENCS_DATABASE_PASSWORD)
        print(self.TOKEN, self.HOST, self.TICKETS, self.T_MAX, self.T_MIN, self.DATABASE_HOST, self.DATABASE_PORT, flush=True)

    def __del__(self):
        if self._hub_connection != None:
            self._hub_connection.stop()

    def __setup_database__(self):
        conn = self.database_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS oxygencs_events (id SERIAL PRIMARY KEY, event VARCHAR NOT NULL, temperature DECIMAL NOT NULL, timestamp TIMESTAMP NOT NULL)")
        conn.commit()
        conn.close()
        cursor.close()

    def setup(self):
        self.__setup_database__()
        self.setSensorHub()
    
    def start(self):
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.", flush=True)
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
        self._hub_connection.on_open(lambda: print("||| Connection opened.", flush=True))
        self._hub_connection.on_close(lambda: print("||| Connection closed.", flush=True))
        self._hub_connection.on_error(lambda data: print(f"||| An exception was thrown closed: {data.error}", flush=True))

    def onSensorDataReceived(self, data):
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            date = data[0]["date"]
            temp = data[0]["data"]
            self.analyzeDatapoint(date, temp)
        except Exception as err:
            print(err, flush=True)

    def analyzeDatapoint(self, date, data):
        if float(data) >= float(self.T_MAX):
            self.sendActionToHvac(date, "TurnOnAc", self.TICKETS)
            event = "Activating AC for " + self.TICKETS + " ticks"
            self.send_event_to_database(event, float(data))
        elif float(data) <= float(self.T_MIN):
            self.sendActionToHvac(date, "TurnOnHeater", self.TICKETS)
            event = "Activating heater for " + self.TICKETS + " ticks"
            self.send_event_to_database(event, float(data))

    def sendActionToHvac(self, date, action, nbTick):
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{nbTick}")
        details = json.loads(r.text)
        print(details, flush=True)

    def send_event_to_database(self, event, temperature):
        try:
            print("Inserting event into database", flush=True)
            print(event, temperature)
            conn = self.database_connection()
            cursor = conn.cursor()
            query = 'INSERT INTO oxygencs_events (event, temperature, timestamp) VALUES (\'' + event + '\', ' + str(temperature) + ', NOW());'
            print(query, flush=True)
            cursor.execute(query)
            conn.commit()
            conn.close()
            cursor.close()
        except requests.exceptions.RequestException as e:
            print("Failed to insert event into database", flush=True)
    
    def database_connection(self):
        conn = psycopg2.connect(
            host = self.DATABASE_HOST,
            port = self.DATABASE_PORT,
            database = self.DATABASE,
            user = self.DATABASE_USERNAME,
            password = self.DATABASE_PASSWORD
        )
        return conn

if __name__ == "__main__":
    main = Main()
    main.start()
