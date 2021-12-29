import json
from django.http import JsonResponse


from django.contrib.auth.models import User

from .models import ChatMessage, Chat


def send_message_api(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            message = data["message"]
            chat = Chat.objects.get(pk=data["chat_id"])
            ChatMessage.objects.create(
                chat=chat, created_by=request.user, message=message
            )
            return JsonResponse({"status": "success", "message": message})
        return JsonResponse({"status": "error"})
    else:
        return JsonResponse({"status": "error"})


def get_message_api(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            to_user = User.objects.get(username=request.GET["to_user"])
            chat = Chat.objects.filter(users__in=[request.user])
            chat = chat.filter(users__in=[to_user])
            chat_messages = ChatMessage.objects.filter(chat=chat[0])
            context = {
                "status": "success",
                "chat": list(chat.values("id", "users", "modified_at")),
                "to_user": to_user.username,
                "messages": list(
                    chat_messages.values(
                        "id", "message", "created_by__username", "created_at"
                    )
                ),
            }
            return JsonResponse(context)
        return JsonResponse({"status": "error"})
    else:
        return JsonResponse({"status": "error"})
