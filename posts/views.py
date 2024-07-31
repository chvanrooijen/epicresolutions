from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Post, Comment
from .forms import CommentForm


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = "posts/post-list.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_date')
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.save()
            return redirect(comment.post.get_absolute_url())
        else:
            # If the form is not valid, render the detail view with form errors.
            self.object = self.get_object()
            context = self.get_context_data(object=self.object, comment_form=form)
            return self.render_to_response(context)


def category_filter(request, pk):
    # Fetch the category by its primary key (pk)
    category = get_object_or_404(Category, pk=pk)
    # Filter posts by the selected category
    posts = Post.objects.filter(categories=category)
    # Render the template with the filtered posts and the category
    return render(request, 'posts/category-filter.html', {'object_list': posts, 'category': category})