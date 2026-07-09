from apps.core.models import Banner

def global_data(request):
    return {"main_banner": Banner.objects.filter(is_active=True).first()}