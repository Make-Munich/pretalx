import importlib
from contextlib import suppress

from django.apps import apps
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from djangosaml2 import views as djangosaml2_views
from django.contrib.auth.decorators import login_required

plugin_patterns = []
for app in apps.get_app_configs():
    if hasattr(app, 'PretalxPluginMeta'):
        if importlib.util.find_spec(app.name + '.urls'):
            urlmod = importlib.import_module(app.name + '.urls')
            single_plugin_patterns = []
            if hasattr(urlmod, 'urlpatterns'):
                single_plugin_patterns += urlmod.urlpatterns
            plugin_patterns.append(
                url(r'', include((single_plugin_patterns, app.label)))
            )

urlpatterns = [
    url(r'^saml2/', include('djangosaml2.urls')),
    url(r'^saml2test/', djangosaml2_views.echo_attributes, name='echo_attributes'),

    url(r'^orga/', include('pretalx.orga.urls', namespace='orga')),
    url(r'^api/', include('pretalx.api.urls', namespace='api')),
    url(r'', include('pretalx.agenda.urls', namespace='agenda')),
    url(r'', include('pretalx.cfp.urls', namespace='cfp')),
    url(r'', include((plugin_patterns, 'plugins'))),

]

if settings.DEBUG:
    with suppress(ImportError):
        import debug_toolbar
        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
