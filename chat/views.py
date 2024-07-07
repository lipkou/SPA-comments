from django.shortcuts import render
from .forms import MessageForm
from .models.messages import Message
from django.core.paginator import Paginator


def home(request):
    page = int(request.GET.get("page", 1))
    sort_type = request.GET.get("sort", "-created")

    # Receive only top messages (not replies)
    messages = Message.objects.filter(reply__isnull=True).order_by(sort_type)
    paginator = Paginator(messages, 20)

    try:
        paginator_mes = paginator.page(page)
    except:
        paginator_mes = paginator.page(1)
    
    message_list = []
    for message in paginator_mes:
        message_data = {
            'id': message.id,
            'user_name': message.user_name,
            'email': message.email,
            'home_page': message.home_page,
            'created': message.created.strftime('%d.%m.%Y %H:%M'),
            'message': message.text,
            'responses': []
        }
        
        # Adding replies to each main post
        responses = message.responses.all().order_by('created')
        response_user = message.user_name
        while responses:
            response_in_responses = []
            for response in responses:
                message_data['responses'].append({
                    'id': response.id,
                    'user_name': response.user_name,
                    'email': response.email,
                    'home_page': response.home_page,
                    'created': response.created.strftime('%d.%m.%Y %H:%M'),
                    'message': response.text,
                    'response_user': response_user
                })
                response_in_responses = response.responses.all().order_by('created')
            response_user = response.user_name
            responses = list(response_in_responses)
        
        message_list.append(message_data)
    
    form = MessageForm()
    context = {
        "form": form, 
        "message_list": message_list,
        "paginator_mes": paginator_mes,
    }
    return render(request, 'chat/index.html', context)
