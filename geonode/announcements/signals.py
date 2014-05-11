import django.dispatch

announcement_published = django.dispatch.Signal(providing_args=["announcement", "request"])
