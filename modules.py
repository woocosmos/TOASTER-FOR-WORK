import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import pandas as pd


def initializer():
    record = pd.read_csv("D:\\work\\toaster\\data\\work_schedule.csv", index_col=0)
    today = datetime.today().date().strftime("%Y-%m-%d")

    if today in record.index:
        # 오늘 날짜의 기록이 이미 존재

        boot_H, boot_M = process_str(record[record.index == today]["booting"].iloc[0])
        goal_rec = record[record.index == today]["goal"].iloc[0]
        off_rec = record[record.index == today]["actual"].iloc[0]

        if pd.isna(goal_rec):
            goal_H, goal_M = ask_goal()
        else:
            goal_H, goal_M = process_str(goal_rec)

    else:
        # 오늘 기록이 없음
        boot_H, boot_M = ask_boot()
        goal_H, goal_M = ask_goal()
        off_rec = None

    Bval = f"{boot_H}:{boot_M}"
    Gval = f"{goal_H}:{goal_M}"
    Aval = None if pd.isna(off_rec) else off_rec

    messagebox.showinfo("목표 퇴근 시간", f"{goal_H}시 {goal_M}분에 알림 예정")

    record.loc[today] = [Bval, Gval, Aval]
    record.to_csv("D:\\work\\toaster\\data\\work_schedule.csv")

    return record


def process_str(INPUT_STRING):
    UHR_dict = {
        "한": 1,
        "두": 2,
        "세": 3,
        "네": 4,
        "다섯": 5,
        "여섯": 6,
        "일곱": 7,
        "여덟": 8,
        "아홉": 9,
        "열": 10,
        "열한": 11,
        "열두": 12,
    }
    MINT_dict = {
        "일": 1,
        "이": 2,
        "삼": 3,
        "사": 4,
        "오": 5,
        "육": 6,
        "칠": 7,
        "팔": 8,
        "구": 9,
        "십": 10,
        "반": 30,
    }

    INPUT_STRING = INPUT_STRING.replace(" ", "")
    INPUT_STRING = INPUT_STRING.replace(":", "시")
    INPUT_STRING = INPUT_STRING.replace("분", "")

    # 숫자로만 이루어진 경우
    if INPUT_STRING.isdigit():
        if len(INPUT_STRING) <= 2:
            UHR = int(INPUT_STRING)
            MINT = 0

        else:
            tmp_UHR = int(INPUT_STRING[:2])
            if tmp_UHR > 25:
                UHR = int(INPUT_STRING[0])
                MINT = int(INPUT_STRING[1:])
            else:
                UHR = tmp_UHR
                MINT = int(INPUT_STRING[2:])

        if (UHR > 24) or (MINT >= 60):
            return (0, 0)

        return (UHR, MINT)

    elif "시" in INPUT_STRING:
        cans = INPUT_STRING.split("시")
        UHR, MINT = cans[0], cans[1]

        if UHR.isdigit() and int(UHR) <= 24:
            UHR = int(UHR)
        elif UHR in UHR_dict.keys():
            UHR = UHR_dict[UHR]

        if MINT.isdigit() and int(MINT) < 60:
            MINT = int(MINT)
        elif len(MINT) == 1:
            MINT = MINT_dict[MINT]
        elif "십" in MINT:
            ten = 1 if not MINT.split("십")[0] else MINT_dict[MINT.split("십")[0]]
            one = 0 if not MINT.split("십")[1] else MINT_dict[MINT.split("십")[1]]
            MINT = ten * 10 + one

        if not MINT:
            MINT = 0
        elif isinstance(MINT, str):
            return (0, 0)

        return (UHR, MINT)

    return (0, 0)


def ask_boot():
    boot = datetime.now()
    return (boot.hour, boot.minute)


def ask_goal():
    ROOT = tk.Tk()
    ROOT.withdraw()

    while True:
        INP = simpledialog.askstring(title="", prompt="몇 시에 퇴근 할 거야?")
        H, M = process_str(INP)
        if H + M > 0:
            break
        messagebox.showinfo("경고", "제대로 써")

    if H < 12:
        H += 12

    return (H, M)
