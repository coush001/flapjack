import uuid
import pandas as pd
from IPython.display import display
import time
import asyncio


pd.options.display.width = 0

def get_uuid():
    return str(uuid.uuid4())[:8]