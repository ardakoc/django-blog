import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from blog.forms import CommentForm
from blog.models import Post


logger = logging.getLogger(__name__)


def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now()).select_related('author').order_by('-published_at')
    logger.debug('Got %d posts', len(posts))
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user.is_active:
        # if user is active
        if request.method == 'POST':
            # if request is POST, create a form using the posted data
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                # save the form. we won't write Comment obj to the db, instead we will
                # return it, using the commit=False arg
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                logger.info(
                    'Created comment on Post %d for user %s',
                    post.pk,
                    request.user
                )
                # perform a redirect back to the current post (refresh the page)
                return redirect(request.path_info)
        else:
            # if request is not POST, create a blank form
            comment_form = CommentForm()
    else:
        # if user is not active
        comment_form = None

    return render(
        request,
        'blog/post-detail.html',
        {'post': post, 'comment_form': comment_form}
    )
