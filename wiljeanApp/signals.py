from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from .models import Contact, replyContact, Blog, Subscription

@receiver(post_save, sender=replyContact)
def send_appointment_email(sender, instance, **kwargs):
    # reply = replyContact.objects.get(id = instance)
    subject = f'reply from {instance.name} at Wiljean Singing Ministry'
    message = instance.message
    contact_email = instance.contact.email
    context = {
        'message': message,
        'date': instance.date,
        'instance':instance,
        # 'contact_date':instance.contact.date 
        
        }

    # Render HTML content from a template
    html_message = render_to_string('wiljeanApp/reply_mail.html', context)

    # Send email
    send_mail(
        subject,
        strip_tags(html_message), 
        'Reply from Wiljean Singing Ministry', 
        [contact_email],
        html_message=html_message,
    )

@receiver(post_save, sender=Blog)
def send_newsletter_email(sender, instance, **kwargs):
    subscribers = Subscription.objects.all()
    email_list = []

    for subscriber in subscribers:
        email_list.append(subscriber.email)

    if email_list:
        subject = 'New blog post at Wiljean Singing Ministry'
        message = f'Hi,\n\nWe have posted a new blog post on our platform'
        message += f' Wiljean Singing Ministry titled "{instance.title}".'
        message += ' You may visit our site to get the full detail. Thank you.'

        context = {
            'instance': instance,
            'unsubscribe_url': reverse('unsubscribe', kwargs={'news_id': instance.id}),
            'message':message
        }
        # Render HTML content from a template
        html_message = render_to_string('wiljeanApp/newsletter.html', context)

        # Send email
        send_mail(
            subject,
            strip_tags(html_message),
            'mathiaswilfred7@gmail.com', #you can put do not reply instead
            email_list,
            html_message=html_message,
        )
