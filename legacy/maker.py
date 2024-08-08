# from PIL import Image

# logo = Image.open("D:\\work\\toaster\\dev\\work.jpg")

# logo.save("D:\\work\\toaster\\dev\\work.ico",format='ICO')


import pandas as pd
from datetime import datetime
from utils import to_datetime

today_index = datetime.today().date()
# today_index = '2023-10-09'
record = pd.read_csv("D:\\work\\toaster\\dev\\work_schedule.csv", index_col=0)

a1 = "10:11"
a2 = None
a3 = None

df = pd.DataFrame(
    [[a1, a2, a3]], index=[today_index], columns=["booting", "goal", "actual"]
)
# test = pd.concat([record, df])

# print(test)
df.to_csv("D:\\work\\toaster\\dev\\work_schedule.csv")
