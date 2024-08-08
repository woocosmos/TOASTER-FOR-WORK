from plyer import notification


def time_to_work():
    notification.notify(
        title="work",
        message="다시 일하러 갈 시간",
        app_name="토스터",
        app_icon="D:\\work\\toaster\\img\\work.ico",
        timeout=10,
    )


def time_to_rest():
    notification.notify(
        title="rest",
        message="휴식 시간",
        app_name="토스터",
        app_icon="D:\\work\\toaster\\img\\rest.ico",
        timeout=10,
    )


def time_to_water():
    notification.notify(
        title="water",
        message="물 마셔!!!!!!!!!!!!!",
        app_name="토스터",
        app_icon="D:\\work\\toaster\\img\\water.ico",
        timeout=5,
    )


def bef_min(last_min):
    msg = f"목표 퇴근 시간까지 {last_min}분 남았습니다."
    if last_min == 0:
        msg = "목표 퇴근 시간이 되었습니다. 정리하고 일어나세요."

    notification.notify(
        title="퇴근 알림",
        message= msg,
        app_name="토스터",
        app_icon="D:\\work\\toaster\\img\\water.ico",
        timeout=10,
    )
