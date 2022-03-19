from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone

from blog.forms import PostForm, CommentForm
from blog.models import Post, Category, Comment


def postlist(request):
    # 포스트 목록
    post_list = Post.objects.order_by('-pub_date')
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    #검색
    if kw:
        post_list = post_list.filter(
            Q(title__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(comment__content__icontains=kw)
        ).distinct()
    # 페이지
    paginator = Paginator(post_list, 5)  #페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page)
    categories = Category.objects.all()
    context = {'post_list':page_obj, 'categories':categories,
               'page':page, 'kw':kw}
    return render(request, 'blog/post_list.html', context)

def detail(request, post_id):
    # 상세 페이지
    post = Post.objects.get(id=post_id)
    categories = Category.objects.all()
    context = {'post':post, 'categories':categories}
    return render(request, 'blog/post_detail.html', context)

def category_page(request, slug):
    # 카테고리
    category = Category.objects.get(slug=slug)
    post_list = Post.objects.filter(category=category)
    categories = Category.objects.all()
    post_list.order_by('-pub_date')

    context = {
        'category': category,
        'post_list': post_list,
        'categories':categories
    }
    return render(request, 'blog/post_list.html', context)

@login_required(login_url='common:login')
def post_create(request):
    # 포스트 등록
    if request.method == "POST":
        # 글과 이미지 각각 가져옴
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  #가저장
            post.pub_date = timezone.now()  #등록일
            post.author = request.user      #작성자
            post.save()                     #db에 저장
            return redirect('blog:postlist')
    else:
        form = PostForm()
    context = {'form':form}
    return render(request, 'blog/post_form.html', context)

@login_required(login_url='common:login')
def post_modify(request, post_id):
    # 포스트 수정
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.modify_date = timezone.now()
            post.author = request.user
            post.save()
            return redirect('blog:detail', post_id=post_id)
    else:
        form = PostForm(instance=post)
    context = {'form':form}
    return render(request, 'blog/post_form.html', context)

@login_required(login_url='common:login')
def post_delete(request, post_id):
    # 포스트 삭제
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('blog:postlist')

@login_required(login_url='common:login')
def comment_create(request, post_id):
    # 댓글 등록
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pub_date = timezone.now()
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog:detail', post_id=post_id)
    else:
        form = CommentForm()
    context = {'form':form}
    return render(request, 'blog/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    # 댓글 삭제
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('blog:detail', post_id=comment.post.id)

@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.author = request.user
            comment.save()
            return redirect('blog:detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form':form}
    return render(request, 'blog/comment_form.html', context)

