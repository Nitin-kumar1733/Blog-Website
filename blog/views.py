from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from decouple import config
import os

# LangChain imports for AI summarization  
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.documents import Document
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)




class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})



@login_required
def summarize_post(request, pk):
    """Generate AI summary for a blog post using LangChain"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if LangChain is available
    if not LANGCHAIN_AVAILABLE:
        messages.error(request, 'AI summarization is not available. Please install required packages.')
        return redirect('post-detail', pk=pk)
    
    # Check if OpenAI API key is configured
    api_key = config('OPENAI_API_KEY', default='')
    if not api_key:
        messages.error(request, 'AI summarization is not configured. Please add OPENAI_API_KEY to environment.')
        return redirect('post-detail', pk=pk)
    
    try:
        # Check if summary already exists and is recent (less than 1 day old)
        if post.summary and post.summary_generated_at:
            time_diff = timezone.now() - post.summary_generated_at
            if time_diff.days < 1:
                messages.info(request, 'Using cached summary from today.')
                return redirect('post-detail', pk=pk)
        
        # Strip HTML tags from content for summarization
        from html import unescape
        import re
        clean_content = re.sub('<[^<]+?>', '', post.content)
        clean_content = unescape(clean_content)
        
        # Initialize LangChain ChatOpenAI
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            max_tokens=200,
            api_key=api_key
        )
        
        # Create prompt using ChatPromptTemplate (LangChain 1.2.7 API)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that creates concise summaries of blog posts."),
            ("user", "Write a concise summary of the following blog post in 2-3 sentences:\n\n{text}\n\nCONCISE SUMMARY:")
        ])
        
        # Create chain using LCEL (LangChain Expression Language)
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        
        # Generate summary using LangChain
        summary = chain.invoke({"text": clean_content})
        
        # Save the summary
        post.summary = summary.strip()
        post.summary_generated_at = timezone.now()
        post.save()
        
        messages.success(request, 'AI summary generated successfully!')
        
    except Exception as e:
        messages.error(request, f'Error generating summary: {str(e)}')
    
    return redirect('post-detail', pk=pk)
