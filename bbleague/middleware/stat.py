import datetime
from base.models import Stat


def stat_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        response = get_response(request)
        print(request.user)
        if(request.user is not None and request.user.id is not None):
            Stat.objects.update_or_create(user_id=request.user.id, defaults={'last_online':datetime.datetime.now()})
        #TODO: Collect more stats here

        return response

    return middleware
