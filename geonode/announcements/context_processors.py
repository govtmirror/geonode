from announcements.models import current_announcements_for_request


def site_wide_announcements(request):
    """
    Adds the site-wide announcements to the global context of templates.
    """
    ctx = {"site_wide_announcements": getActiveAnnouncements(request, site_wide=True)}
    return ctx
