from django.contrib import admin

from .models import Jury, Panel, Message, Number

# ...

admin.site.register(Jury)
admin.site.register(Panel)
admin.site.register(Message)
admin.site.register(Number)
