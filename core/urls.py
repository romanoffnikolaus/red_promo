from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='RED_PROMO',
        description='Оффлайн библиотека',
        default_version='v1'
    ), public=True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger')),
    path('', include('applications.account.urls')),
    path('', include('applications.books.urls')),
    path('', include('applications.rent.urls')),
    path('', include('applications.import_csv.urls')),
    path('__debug__/', include('debug_toolbar.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)