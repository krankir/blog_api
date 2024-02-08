from __future__ import absolute_import, unicode_literals

import datetime
from django.utils import timezone


from celery.task import periodic_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from blog.models import Post

User = get_user_model()


@periodic_task(run_every=(datetime.timedelta(days=1)), name="first_periodic")
def send_daily_post_digest():
    """Раз в сутки на почту прилетает подборка из 5 последних постов ленты."""
    start_time = timezone.now() - datetime.timedelta(days=1)
    end_time = timezone.now()
    subscribed_users = User.objects.filter(subscribed_to_newsletter=True)
    for user in subscribed_users:
        subscribed_users_subquery = User.objects.filter(following__user=user).values(
            "id"
        )
        posts = Post.objects.filter(
            author_id__in=subscribed_users_subquery,
            pub_date__range=(start_time, end_time),
        ).order_by("-pub_date")[:5]
        list_posts = list([post.title for post in posts])
        text_mail = str(list_posts)
        email_to = user.email
        send_mail(
            "рассылка 5 последних постов ленты",
            text_mail,
            "admin@example.com",
            [
                email_to,
            ],
            fail_silently=False,
        )
