from app.db.models import MemoryInfo
import json
from pyModbusTCP.client import ModbusClient


def read_register(modbus_client, registro, retries=0):
    regs = modbus_client.read_holding_registers(registro, 1)#1540 #22123
    if regs:
        return regs
    else:

        if retries > 0:
            for i in range(1, retries):
                regs = modbus_client.read_holding_registers(registro, 1)
                if regs:
                    return regs

        print("read modbus error")
        return None


def write_register(modbus_client, registro, valor):
    regs = modbus_client.write_single_register(reg_addr=registro, reg_value=valor)
    if regs:
        return regs
    else:
        print("read modbus error")
        return False


def process_memory_test_result(payload:MemoryInfo, modbus:ModbusClient):

    modbus_registro_old = read_register(modbus_client=modbus, registro=int(payload.modbus_register), retries=3)
    r = write_register(modbus_client=modbus,registro=int(payload.modbus_register), valor=payload.modbus_register_value)
    if not r:
        print("Failed to write")
    modbus_registro = read_register(modbus_client=modbus, registro=int(payload.modbus_register))
    resp = {"msg": "OK", "memory_id": payload.memory_id, "registro": str(payload.modbus_register), "old_value": modbus_registro_old, "new_value": modbus_registro}

    return json.dumps(resp), None
