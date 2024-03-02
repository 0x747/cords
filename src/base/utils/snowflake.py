import time
from datetime import datetime, timedelta

class Snowflake():

    def __init__(self):
        self.data_center_id = 0
        self.worker_id = 0
        self.sequence = 0
        self.last_timestamp = 0

        self.EPOCH = 1288834974657
        self.SEQUENCE_BITS = 12
        self.WORKER_BITS = 5
        self.DATA_CENTER_BITS = 5

        self.MAX_WORKER_ID = 0b11111
        self.MAX_DATA_CENTER_ID = 0b11111

        self.WORKER_SHIFT = self.SEQUENCE_BITS #12
        self.DATA_CENTER_SHIFT = self.SEQUENCE_BITS + self.WORKER_BITS #17
        self.TIMESTAMP_SHIFT = self.SEQUENCE_BITS + self.WORKER_BITS + self.DATA_CENTER_BITS #23


    def _get_current_timestamp(self) -> int:
        return int(time.time() * 1000)
    
    def _wait_for_next_timestamp(self, last_timestamp: int) -> int:
        timestamp = self._get_current_timestamp()

        while timestamp <= last_timestamp:
            ("same again")
            timestamp = self._get_current_timestamp()
        
        return timestamp
    
    def generate_id(self) -> int:

        timestamp = self._get_current_timestamp()

        if timestamp < self.last_timestamp:
            raise Exception("Current timestamp is less than last timestamp. Travelling back in time is not allowed!")
        
        if timestamp == self.last_timestamp:
            print("same")
            self.sequence = (self.sequence + 1) & (1 << self.SEQUENCE_BITS - 1)

            if not self.sequence:
                timestamp = self._wait_for_next_timestamp(self.last_timestamp)
        else:
            self.sequence = 0
        
        self.last_timestamp = timestamp

        snowflake_id = ((timestamp - self.EPOCH) << self.TIMESTAMP_SHIFT) | (self.data_center_id << self.DATA_CENTER_SHIFT) | (self.worker_id << self.WORKER_SHIFT) | self.sequence
        
        return snowflake_id
    
    def id_to_date(self, snowflake_id: int) -> str:
        timestamp = (snowflake_id >> self.TIMESTAMP_SHIFT) + self.EPOCH
        milliseconds = snowflake_id & ((1 << self.TIMESTAMP_SHIFT) - 1)
        seconds = timestamp // 1000
        date = datetime.fromtimestamp(seconds) + timedelta(milliseconds=milliseconds)

        return date.strftime('%Y-%m-%d %H:%M:%S.%f')

    def id_to_dateUS(self, snowflake_id: int) -> str:
            timestamp = (snowflake_id >> self.TIMESTAMP_SHIFT) + self.EPOCH
            milliseconds = snowflake_id & ((1 << self.TIMESTAMP_SHIFT) - 1)
            seconds = timestamp // 1000
            date = datetime.fromtimestamp(seconds) + timedelta(milliseconds=milliseconds)

            # Format the datetime object in the desired custom format
            custom_date_format = date.strftime('%B %d, %Y')
            
            return custom_date_format
