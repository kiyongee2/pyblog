from django.shortcuts import render

from blog.models import Post


def index(request):
    recent_post = Post.objects.order_by('-pk')[:3]
    context = {'recent_post': recent_post}
    return render(request, 'aboutme/index.html', context)

def profile(request):
    return render(request, 'aboutme/profile.html')