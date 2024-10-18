from django.shortcuts import render
from django.shortcuts import redirect
from .models import Panel, Jury, User, Message
from .forms import *
from .text import text
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import *


@login_required
def home(request):
    first = False
    jury_list = Jury.objects.filter(judge=request.user)
    jury_form = JuryCreate()
    message_form = MessageForm()
    panels = Panel.objects.all()
    if request.method == "POST":
        if 'jury_form' in request.POST:
            form = JuryCreate(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                jury = Jury.objects.create(judge=request.user, casename=data["casename"])
                for x in range(1, (data.get('panel_num')+1)):
                    Panel.objects.create(jury=jury, number=x)
    user = User.objects.get(username=request.user)
    diff = (datetime.now(timezone.utc) - user.date_joined)
    print(diff)
    if diff.seconds < 20:
        first = True
    else:
        first = False
    return render(request, "home.html", {"jury_list": jury_list, "jury_form": jury_form, "message_form": message_form, "panels": panels, "first": first})

@login_required
def send_all(request, jury):
    if request.method == "POST":
        if 'message_form' in request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.judge = request.user
                message_jury = Jury.objects.get(pk=jury)
                message_panel = Panel.objects.filter(jury=message_jury)
                user = User.objects.get(username=request.user)
                message.save()
                for x in message_panel:
                    message.panel.add(x)
                    for member in x.members.all():
                            text(member, message, user.last_name)
                            pass
        if 'jury_form' in request.POST:
            form = JuryCreate(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                jury = Jury.objects.create(judge=request.user, casename=data["casename"])
                for x in range(1, (data.get('panel_num')+1)):
                    Panel.objects.create(jury=jury, number=x)
    jury_form = JuryCreate()
    message_form = MessageForm()
    jury_list = Jury.objects.filter(judge=request.user)
    jury = Jury.objects.get(pk=jury)
    panels = Panel.objects.filter(jury=jury)
    query = Message.objects.none()
    members = Number.objects.none()
    for panel in panels:
        query = query.union(Message.objects.filter(panel=panel)).order_by('-timestamp')
        members = members.union(panel.members.all())
    paginator = Paginator(query, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {"jury_list": jury_list, "jury_form": jury_form, "message_form": message_form, "jury": jury, "messages": page_obj, "panels":Panel.objects.all(), "page":0, "members":members})

@login_required
def send_panel(request, jury, panel_num):
    if request.method == "POST":
        if 'message_form' in request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.judge = request.user
                message_jury = Jury.objects.get(pk=jury)
                message_panel = Panel.objects.get(jury=message_jury, number=panel_num)
                message.save()
                message.panel.add(message_panel)
                user = User.objects.get(username=request.user)
                for member in message_panel.members.all():
                         text(member, message, user.last_name)
                         pass
        if 'jury_form' in request.POST:
            form = JuryCreate(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                jury = Jury.objects.create(judge=request.user, casename=data["casename"])
                for x in range(1, (data.get('panel_num')+1)):
                    Panel.objects.create(jury=jury, number=x)
    jury_form = JuryCreate()
    message_form = MessageForm()
    jury_list = Jury.objects.filter(judge=request.user)
    jury = Jury.objects.get(pk=jury)
    panels = Panel.objects.all()
    panel = Panel.objects.get(jury=jury, number=panel_num)
    query = Message.objects.filter(panel=panel).order_by('-timestamp')
    members = panel.members.all()
    paginator = Paginator(query, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    link = "https://www.court-connect.net/add/" + str(panel.id)
    return render(request, "home.html", {"jury_list": jury_list, "jury_form": jury_form, "message_form": message_form, "jury": jury, "messages": page_obj, "panels":panels, "qrcode_panel":panel, "page":int(panel_num), "members":members, "link": link})

def add_number(request, panel):
    if request.method == "POST":
        print("POST")
        form = AddJuror(request.POST)
        if form.is_valid():
            print("VALID")
            juror = form.save(commit=False)
            juror.save()
            juror_panel = Panel.objects.get(pk=panel)
            juror_panel.members.add(juror)
            number = juror.pk
            return redirect('juryapp:dash', panel, number)
    form = AddJuror()
    return render(request, "add_juror.html", {"form": form})

def dash(request, panel, number):
    dash_panel = Panel.objects.get(pk=panel)
    panel_num = dash_panel.number
    number = Number.objects.get(pk=number)
    return render(request, "dash.html", {"number": number, "panel_num": panel_num})

def qr(request, panel):
    panel = Panel.objects.get(pk=panel)
    jury = Jury.objects.get(pk=panel.jury.pk)
    panel_num = panel.number
    url = ("https://juryapp-production.up.railway.app/add/"+str(panel.pk))
    return render(request, "qrcode.html", {"link":url, "panel_num":panel_num, "jury":jury, "top_nav": True})

def register(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('juryapp:home'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def delete(request, jury):
     jury = Jury.objects.get(pk=jury)
     jury.delete()
     return redirect('juryapp:home')

def delete_number(request, member, jury):
     number = Number.objects.get(pk=member)
     number.delete()
     jury=Jury.objects.get(pk=jury)
     return redirect('juryapp:send_all', jury.pk)

def settings(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UpdateUserForm(initial={'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name})
    return render(request, 'settings.html', {'form': form})