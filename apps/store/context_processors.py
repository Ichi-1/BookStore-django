from .models import Category

def categories(request):
    return {
        'categories': Category.objects.all()
        # filter(level=0) for root categories only in dropdown menu
    }