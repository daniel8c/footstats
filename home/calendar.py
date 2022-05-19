import datetime
from home.models import MatchResult

# OBLICZANIE NASTEPNEGO WTORKU OD TERAZ
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    next_tuesday = d + datetime.timedelta(days_ahead) # NASTEPNY WTOREK
    prev_tuesday = next_tuesday-datetime.timedelta(7) # poprzedni wtorek

    return prev_tuesday, next_tuesday

d = datetime.date.today()
zakres = next_weekday(d, 1) # 0 = Monday, 1=Tuesday, 2=Wednesday...
print(zakres)
object_list = models.MatchResult
print(object_list)
