from .models import Brands

def brand_list(request):
    return {
       'all_brands': Brands.objects.all()
    }