from django.urls import path
from .views import *
from django.conf.urls import include, url

app_name = "juryapp"

urlpatterns = [
    path("jury/<jury>/<panel_num>/", send_panel, name="send_panel"),
    path("jury/<jury>/", send_all, name="send_all"),
    path("", create_jury, name="create"),
    path("add/<panel>/", add_number, name="add_juror"),
    path("dash/<panel>/", dash, name="dash"),
    path("qr/<panel>/", qr, name="qr"),
    url(r"^register/", register, name="register"),
]