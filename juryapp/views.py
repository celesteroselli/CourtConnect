from django.shortcuts import render
from django.shortcuts import redirect
from .models import Panel, Jury, User, Message
from .forms import *
from .text import text
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def send_all(request, jury):
    if request.method == "POST":
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.judge = request.user
                message_jury = Jury.objects.get(pk=jury)
                panels = Panel.objects.filter(jury=message_jury)
                message.save()
                for panel in panels:
                    message.panel.add(panel)
                    for member in panel.members.all():
                         text(member, message)
                         pass
    form = MessageForm()
    jury = Jury.objects.get(pk=jury)
    panels = Panel.objects.filter(jury=jury)
    query = Message.objects.none()
    for panel in panels:
         query = query.union(Message.objects.filter(panel=panel)).order_by('-timestamp')
    return render(request, "home.html", {"form": form, "jury": jury, "messages": query, "panels":panels, "page":0})

@login_required
def send_panel(request, jury, panel_num):
    if request.method == "POST":
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.judge = request.user
                message_jury = Jury.objects.get(pk=jury)
                message_panel = Panel.objects.get(jury=message_jury, number=panel_num)
                message.save()
                message.panel.add(message_panel)
                for member in message_panel.members.all():
                         text(member, message)
                         pass
    form = MessageForm()
    jury = Jury.objects.get(pk=jury)
    panels = Panel.objects.filter(jury=jury)
    panel = Panel.objects.get(jury=jury, number=panel_num)
    query = Message.objects.filter(panel=panel).order_by('-timestamp')
    return render(request, "home.html", {"form": form, "jury": jury, "messages": query, "panels":panels, "qrcode_panel":panel, "page":int(panel_num)})

@login_required
def create_jury(request):
    if request.method == "POST":
            form = JuryCreate(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                jury = Jury.objects.create(judge=request.user)
                for x in range(1, (data.get('panel_num')+1)):
                    Panel.objects.create(jury=jury, number=x)
    form = JuryCreate()
    list = Jury.objects.filter(judge=request.user)
    return render(request, "create.html", {"form": form, "list": list})

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
            return redirect('juryapp:dash', panel)
    form = AddJuror()
    return render(request, "add_juror.html", {"form": form})

def dash(request, panel):
    messages = Message.objects.filter(panel=panel)
    dash_panel = Panel.objects.get(pk=panel)
    return render(request, "dash.html", {"messages": messages, "panel": dash_panel})

def qr(request, panel):
    panel = Panel.objects.get(pk=panel)
    jury = Jury.objects.get(pk=panel.jury.pk)
    panel_num = panel.number
    url = ("https://juryapp-production.up.railway.app/add/"+str(panel.pk))
    return render(request, "qrcode.html", {"link":url, "panel_num":panel_num, "jury":jury})

def register(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('juryapp:create'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})