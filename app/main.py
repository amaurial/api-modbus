from fastapi import FastAPI, HTTPException
from app.db.models import MemoryInfo
from app.api.memory_test import process_memory_test_result
from pyModbusTCP.client import ModbusClient


def connect_modbus(host, port):
    try:
        modbus_client = ModbusClient(host, port, unit_id=255, auto_open=True)
        modbus_client.open()
        print("Connected to CLP")
        return modbus_client
    except Exception as e:
        raise e


app = FastAPI()

MODBUS_IP = "192.168.0.5"
MODBUS_PORT = 502
modbus = connect_modbus(host=MODBUS_IP, port=MODBUS_PORT)

@app.get("/")
def root():
    return {"message": "Memory check api"}

@app.post("/test_result", status_code=201)
def test_result(payload: MemoryInfo):
    print(payload)
    result, error = process_memory_test_result(payload, modbus)
    if not result:
        raise HTTPException(status_code=400, detail=error)
    return result

