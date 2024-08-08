from threading import Timer
import time
import multiprocessing
from datetime import datetime

from api import *
from modules import *
from config import *


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def timer_runner(popf, every):
    print(f"start the timer every {every} minutes")
    func = RepeatTimer(every * 60, popf)
    func.start()


def time_checker(df):
    global before_end
    
    # init
    today = datetime.today().date().strftime("%Y-%m-%d")
    goal = df.loc[today]["goal"]
    boot = df.loc[today]["booting"]

    hr, minute = process_str(goal)

    before_end.append(0)
    before_end = sorted(before_end)[::-1]
    k = 0

    while True:
        now = datetime.now()
        off = f"{now.hour}:{now.minute}"
        df.loc[today] = [boot, goal, off]
        df.to_csv("D:\\work\\toaster\\data\\work_schedule.csv")
    
        just_before = before_end[k]
        
        if now.hour == hr and now.minute == minute - just_before:
            bef_min(just_before)
            k+=1
            if k == len(before_end):
                # reset the turn
                k = 0

        # 30초마다 체크
        time.sleep(30)



if __name__ == "__main__":
    import traceback

    try:
        record = initializer()
        wait = working_minute+resting_minute

        ticker = multiprocessing.Process(target=time_checker, args=((record,)))
        ticker.start()

        water_timer = multiprocessing.Process(target=timer_runner, args=(time_to_water, water_minute))
        work_timer = multiprocessing.Process(target=timer_runner, args=(time_to_work, wait))
        rest_timer = multiprocessing.Process(target=timer_runner, args=(time_to_rest, wait))

        water_timer.start()
        work_timer.start()
        
        time.sleep(working_minute*60)
        time_to_rest()
        rest_timer.start()


    except Exception as e:
        traceback.print_exception(e)
        print('error occurred')
        wait_for_it = input('Press enter to close the terminal window')