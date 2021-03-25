from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (CreateView, DetailView, FormView, TemplateView, ListView)
from django.urls import reverse_lazy

from . forms import TopicCreateForm, TopicModelForm, CommentModelForm
from . models import Topic, Category, Comment, VoteManager, Vote
from django.db.models import Count

class TopicCreateView(CreateView):
    template_name = 'thread/create_topic.html'
    form_class = TopicModelForm
    model = Topic
    success_url = reverse_lazy('base:top')

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'thread/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'thread/create_topic.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('base:top'))

def topic_create(request):
    template_name = 'thread/create_topic.html'
    ctx = {}
    if request.method == 'GET':
        ctx['form'] = TopicCreateForm()
        return render(request, template_name, ctx)
    
    if request.method == 'POST':
        topic_form = TopicCreateForm(request.POST)
        if topic_form.is_valid():
            topic_form.save()
            # topic = Topic()
            # cleaned_data = topic_form.cleaned_data
            # topic.title = cleaned_data['title']
            # topic.message = cleaned_data['message']
            # topic.user_name = cleaned_data['user_name']
            # topic.category = cleaned_data['category']
            # topic.save()   
            return redirect(reverse_lazy('base:top'))
        else:
            ctx['form'] = topic_form
            return render(request, template_name, ctx)

# from . models import Topic
# class TopicDetailView(DetailView):
#   template_name = 'thread/detail_topic.html'
#   model= Topic
#   context_object_name = 'topic'

class CategoryView(ListView):
    template_name = 'thread/category.html'
    context_object_name = 'topic_list'
    paginate_by = 1 # 1ページに表示するオブジェクト数 サンプルのため1にしています。
    page_kwarg = 'p' # GETでページ数を受けるパラメータ名。指定しないと'page'がデフォルト

    def get_queryset(self):
        return Topic.objects.filter(category__url_code = self.kwargs['url_code'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = get_object_or_404(Category, url_code=self.kwargs['url_code'])
        return ctx

class TopicAndCommentView(FormView):
    template_name = 'thread/detail_topic.html'
    form_class = CommentModelForm

    def form_valid(self, form):
        # comment = form.save(commit=False)
        # comment.topic = Topic.objects.get(id=self.kwargs['pk'])
        # comment.no = comment.objects.filter(topic=self.kwargs['pk']).count() + 1
        # comment.save()
        # Comment.objects.create_comment(
        #     user_name=form.cleaned_data['user_name'],
        #     message=form.cleaned_data['message'],
        #     topic_id=self,kwargs['pk'],
        # )
        form.save_with_topic(self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('thread:topic', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['topic'] = Topic.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = Comment.objects.filter(
            topic_id=self.kwargs['pk']).annotate(vote_count=Count('vote')).order_by('no')
        return ctx


# Create your views here.
