from math import ceil
from datetime import datetime, timedelta
from typing import Optional, Union, Dict


def review(
    quality: int,
    easiness: float,
    #interval: int, ---Dear person who made the SM2 algorithm package. Why on earth do you require this as a parameter if you're going to do nothing with it?
    repetitions: int,
    review_datetime: Optional[Union[datetime, str]] = None,
) -> Dict:
    interval: int = 0 #Declaring it instead. THIS DIDN'T NEED TO BE A PARAMETER!
    if not review_datetime:
        review_datetime = datetime.utcnow().isoformat(sep=" ", timespec="seconds")

    if isinstance(review_datetime, str):
        review_datetime = datetime.fromisoformat(review_datetime).replace(microsecond=0)

    if quality < 3:
        interval = 1
        repetitions = 0
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = ceil(interval * easiness)

        repetitions += 1

    easiness += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    if easiness < 1.3:
        easiness = 1.3

    review_datetime = review_datetime + timedelta(days=interval)

    return {
        "easiness": easiness,
        "interval": interval,
        "repetitions": repetitions,
        "review_datetime": review_datetime.strftime('%Y-%m-%d %H:%M:%S.%f') #For consistency with First_review()'s output.
    }


def first_review(
    quality: int,
    review_datetime: Optional[Union[datetime, str]] = None,
) -> Dict:
    if not review_datetime:
        review_datetime = datetime.utcnow()

    return review(quality, 2.5, 0, review_datetime)
