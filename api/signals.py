import datetime
from django.contrib.auth.signals import user_logged_in

from base.models import Stat


def collect_stat(sender, user, request, **kwargs):
    if(user is None or user.id is None):
        return
    stat,_ = Stat.objects.get_or_create(user_id=user.id)
    times_logged_in = stat.times_logged_in
    if (times_logged_in is None):
        times_logged_in = 0
    Stat.objects.update_or_create(
        user_id=user.id, defaults={'times_logged_in':times_logged_in+1, 'last_login':datetime.datetime.now()})


user_logged_in.connect(collect_stat)
