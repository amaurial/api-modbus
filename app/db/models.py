from pydantic import BaseModel, validator
from typing import List
from datetime import datetime

class MemoryInfo(BaseModel):
    memory_id: str
    processing_timestamp: str
    test_result: str
    modbus_register: int
    modbus_register_value: int

    @validator('processing_timestamp')
    def is_valid_date(cls, v):
        try:
            # try to convert the string to datetime
            dt = datetime.strptime(v, '%d/%m/%Y %H:%M:%S')
        except Exception as e:
            raise ValueError(f"processing timestamp should be of format DD/MM/YYYY HH:MM:SS {v}. {e}")
