from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def conversation_list(request):
    conversations = request.user.conversations.all()
    return render(request, "chat/conversation_list.html", {"conversations": conversations})

@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.method == "POST":
        text = request.POST.get("message")
        if text:
            Message.objects.create(conversation=conversation, sender=request.user, text=text)
            return redirect("conversation_detail", pk=pk)
    messages = conversation.messages.order_by("timestamp")
    return render(request, "chat/conversation_detail.html", {"conversation": conversation, "messages": messages})

@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)
        conversation.participants.add(other_user)
    return redirect("conversation_detail", pk=conversation.pk)
