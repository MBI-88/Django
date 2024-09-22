from django.urls import re_path
from . import consumers

# Patterns

websocker_urlpatterns = [
    re_path(r'ws/chat/room/(?P<course_id>\d+)/$',consumers.ChatCounsumer.as_asgi()),
    
]