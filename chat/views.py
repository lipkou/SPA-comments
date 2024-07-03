from django.shortcuts import render
from .forms import MessageForm
from .models.messages import Message
from django.core.paginator import Paginator


def home(request):
    page = int(request.GET.get("page", 1))
    sort_type = request.GET.get("sort_type", "-created")

    
    messages = Message.objects.all().order_by(sort_type)
    paginator = Paginator(messages, 20)

    
    try:
        paginator_mes = paginator.page(page)
    except:
        paginator_mes = paginator.page(1)
    
    message_list = []
    for message in paginator_mes:
        message_list.append({
            'user_name': message.user_name,
            'email': message.email,
            'home_page': message.home_page,
            'created': message.created.strftime('%d.%m.%Y %H:%M'),
            'message': message.text,
        })
    
    form = MessageForm()
    context = {
        "form":form, 
        "message_list":message_list,
        "paginator_mes":paginator_mes,
    }
    return render(request, 'chat/index.html', context)