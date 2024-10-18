from django.urls import path
from .views import *
from django.conf.urls import include, url

app_name = "juryapp"

urlpatterns = [
    path("jury/<jury>/<panel_num>/", send_panel, name="send_panel"),
    path("jury/<jury>/", send_all, name="send_all"),
    path("", home, name="home"),
    path("add/<panel>/", add_number, name="add_juror"),
    path("dash/<panel>/<number>/", dash, name="dash"),
    path("delete/<jury>/", delete, name="delete"),
    path("delete/<member>/<jury>/", delete_number, name="delete_number"),
    path("settings", settings, name="settings"),
    url(r"^register/", register, name="register"),
]