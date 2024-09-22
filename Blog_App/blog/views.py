from django.shortcuts import get_object_or_404, render
from .models import Post
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


# Create your views here.

def post_list(request:str,tag_slug=None) -> render:
    object_list = Post.published.all()
    #paginator = Paginator(object_list,3) # 3 post per page
    page = request.GET.get('page')
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    
    paginator = Paginator(object_list,3) # 3 post per page
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request,'blog/post/list.html',{'page':page,'posts':posts,'tag':tag}) 
    
    
# Vistas genericas hace lo mismo que la vista post_list

"""
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
"""



# El metodo save() esta en la clase ModelForm pero no en la Form
def post_detail(request:str,year:int,month:int,day:int,post:str) -> render:
    post = get_object_or_404(Post,slug=post,status='published',
                             publish__year=year,publish__month=month,
                             publish__day=day)
    
    comments = post.comments.filter(active=True) 
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4] 
    
    return render(request,'blog/post/detail.html',
                  {'post':post,
                   'comments':comments,
                   'new_comment':new_comment,
                   'comment_form':comment_form,
                   'similar_posts':similar_posts})


def post_share(request:str,post_id:int) -> render:
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False
    
    if (request.method == 'POST'):
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd  = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject,message,'admin@blog.com',[cd['to']],fail_silently=False)
            sent = True
    
    else:
        form = EmailPostForm()
        
    return render(request,'blog/post/share.html',
                  {'post':post,
                   'form':form,
                   'sent':sent})


def post_search(request:str) -> render:
    form = SearchForm()
    query = None
    response = []
    if ('query' in request.GET):
        form = SearchForm(request.GET)
        if (form.is_valid()):
            query = form.cleaned_data['query']
            response = Post.published.filter(body__icontains=query)
            response = response.annotate(count_found=Count('body')).order_by('-count_found','-publish')[:3]
    
    return render(request,'blog/post/search.html',{'form':form,'query':query,'response':response})


