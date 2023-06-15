from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# Standard Python Library imports.
from functools import reduce
import operator

# Core Django imports.
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    DetailView,
    ListView, UpdateView, CreateView, View
)

# Blog application imports.
from blog.models import Article, Category, Comment
from blog.forms import CommentForm


class ArticleListView(ListView):
    context_object_name = "articles"
    paginate_by = 12
    queryset = Article.objects.filter(status=Article.PUBLISHED, deleted=False)
    template_name = "site/blog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'site/blog/article.html'

    def get_context_data(self, **kwargs):
        session_key = f"viewed_article {self.object.slug}"
        if not self.request.session.get(session_key, False):
            self.object.views += 1
            self.object.save()
            self.request.session[session_key] = True

        kwargs['related_articles'] = \
            Article.objects.filter(
                category=self.object.category, status=Article.PUBLISHED).order_by('?')[:3]
        kwargs['article'] = self.object
        kwargs['comment_form'] = CommentForm()
        return super().get_context_data(**kwargs)


class ArticleSearchListView(ListView):
    model = Article
    paginate_by = 12
    context_object_name = 'search_results'
    template_name = "blog/article/article_search_list.html"

    def get_queryset(self):
        """
        Search for a user input in the search bar.
        It pass in the query value to the search view using the 'q' parameter.
        Then in the view, It searches the 'title', 'slug', 'body' and fields.
        To make the search a little smarter, say someone searches for
        'container docker ansible' and It want to search the records where all
        3 words appear in the article content in any order, It split the query
        into separate words and chain them.
        """

        query = self.request.GET.get('q')

        if query:
            query_list = query.split()
            search_results = Article.objects.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(slug__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(body__icontains=q) for q in query_list))
            )

            if not search_results:
                messages.info(self.request, f"No results for '{query}'")
                return search_results.filter(status=Article.PUBLISHED, deleted=False)
            else:
                messages.success(self.request, f"Results for '{query}'")
                return search_results.filter(status=Article.PUBLISHED, deleted=False)
        else:
            messages.error(
                self.request, f"Sorry you did not enter any keyword")
            return []

    def get_context_data(self, **kwargs):
        """
            Add categories to context data
        """
        context = super(ArticleSearchListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        return context


class TagArticlesListView(ListView):
    """
        List articles related to a tag.
    """
    model = Article
    paginate_by = 12
    context_object_name = 'tag_articles_list'
    template_name = 'site/blog/tag_articles_list.html'

    def get_queryset(self):
        """
            Filter Articles by tag_name
        """

        tag_name = self.kwargs.get('tag_name', '')

        if tag_name:
            tag_articles_list = Article.objects.filter(tags__name__in=[tag_name],
                                                       status=Article.PUBLISHED,
                                                       deleted=False
                                                       )

            if not tag_articles_list:
                messages.info(self.request, f"No Results for '{tag_name}' tag")
                return tag_articles_list
            else:
                messages.success(self.request, f"Results for '{tag_name}' tag")
                return tag_articles_list
        else:
            messages.error(self.request, "Invalid tag")
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        return context


class CategoryArticlesListView(ListView):
    model = Article
    paginate_by = 12
    context_object_name = 'articles'
    template_name = 'site/blog/category_articles.html'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Article.objects.filter(category=category, status=Article.PUBLISHED, deleted=False)

    def get_context_data(self, **kwargs):
        context = super(CategoryArticlesListView,
                        self).get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context['category'] = category
        return context


class CategoriesListView(ListView):
    model = Category
    paginate_by = 12
    context_object_name = 'categories'
    template_name = 'site/blog/categories_list.html'

    def get_queryset(self):
        return Category.objects.order_by('-date_created')


class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    fields = ["name", "image"]
    template_name = 'site/blog/category_form.html'

    def form_valid(self, form):
        form.instance.save()
        messages.success(self.request, f"'{form.instance.name}' "
                                       f"submitted successfully. You will be "
                                       f"notified when it is approved."
                                       f"Thank you !!!")
        return redirect('/')


class CategoryUpdateCreateView(LoginRequiredMixin, SuccessMessageMixin,
                               UpdateView):
    model = Category
    fields = ["name", "image"]
    template_name = 'site/blog/category_form.html'
    success_url = reverse_lazy("blog:categories_list")
    success_message = "Category Updated Successfully"


class CommentCreateView(CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = get_object_or_404(Article,
                                            slug=self.kwargs.get('slug'))
        comment.save()
        messages.success(self.request, "Comment Added successfully")
        return redirect('blog:article_comments', comment.article.slug)


class ArticleCommentList(ListView):
    context_object_name = "comments"
    paginate_by = 10
    template_name = "site/blog/article_comments.html"

    def get_queryset(self):
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        queryset = Comment.objects.filter(article=article)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArticleCommentList, self).get_context_data(**kwargs)
        context['article'] = get_object_or_404(Article,
                                               slug=self.kwargs.get('slug'))
        context['comment_form'] = CommentForm
        return context


class ArticleWriteView(LoginRequiredMixin, View):

    SAVE_AS_DRAFT = "SAVE_AS_DRAFT"
    PUBLISH = "PUBLISH"

    template_name = 'dashboard/author/article_create_form.html'
    context_object = {}

    def get(self, request, *args, **kwargs):

        article_create_form = ArticleCreateForm()
        self.context_object["article_create_form"] = article_create_form

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        article_create_form = ArticleCreateForm(request.POST, request.FILES)

        action = request.POST.get("action")
        article_status = request.POST["status"]

        if action == self.SAVE_AS_DRAFT:

            if article_status == Article.PUBLISHED:
                self.context_object["article_create_form"] = article_create_form
                messages.error(request,
                               "You saved the article as draft but selected "
                               "the status as 'PUBLISHED'. You can't save an "
                               "article whose status is 'PUBLISHED' as draft. "
                               "Please change the status to 'DRAFT' before you "
                               "save the article as draft.")
                return render(request, self.template_name, self.context_object)

            if article_create_form.is_valid():

                new_article = article_create_form.save(commit=False)
                new_article.author = request.user
                new_article.date_published = None
                new_article.save()
                article_create_form.save_m2m()

                messages.success(request, f"Article drafted successfully.")
                return redirect("blog:drafted_articles")

            self.context_object["article_create_form"] = article_create_form
            messages.error(request, "Please fill required fields")
            return render(request, self.template_name, self.context_object)

        if action == self.PUBLISH:

            if article_status == Article.DRAFTED:
                self.context_object["article_create_form"] = article_create_form

                messages.error(request,
                               "You clicked on 'PUBLISH' to publish the article"
                               " but selected the status as 'DRAFT'. "
                               "You can't Publish an article whose status is "
                               "'DRAFT'. Please change the status to "
                               "'PUBLISHED' before you can Publish the "
                               "article.")
                return render(request, self.template_name, self.context_object)

            if article_create_form.is_valid():
                new_article = article_create_form.save(commit=False)
                new_article.author = request.user
                new_article.save()
                article_create_form.save_m2m()

                messages.success(
                    self.request, f"Article published successfully.")
                return redirect(to="blog:dashboard_article_detail", slug=new_article.slug)

            self.context_object["article_create_form"] = article_create_form
            messages.error(request, "Please fill required fields")
            return render(request, self.template_name, self.context_object)


class ArticleUpdateView(LoginRequiredMixin, View):

    SAVE_AS_DRAFT = "SAVE_AS_DRAFT"
    PUBLISH = "PUBLISH"

    template_name = 'dashboard/author/article_update_form.html'
    context_object = {}

    def get(self, request, *args, **kwargs):

        old_article = get_object_or_404(Article, slug=self.kwargs.get("slug"))
        article_update_form = ArticleUpdateForm(instance=old_article, initial={
                                                'tags': old_article.tags.names})

        self.context_object["article_update_form"] = article_update_form
        self.context_object["article"] = old_article
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        old_article = get_object_or_404(Article, slug=self.kwargs.get("slug"))
        article_update_form = ArticleCreateForm(
            request.POST, request.FILES, instance=old_article)

        action = request.POST.get("action")
        article_status = request.POST["status"]

        if action == self.SAVE_AS_DRAFT:

            if article_status == Article.PUBLISHED:
                self.context_object["article_update_form"] = article_update_form
                messages.error(request,
                               "You saved the article as draft but selected "
                               "the status as 'PUBLISHED'. You can't save an "
                               "article whose status is 'PUBLISHED' as draft. "
                               "Please change the status to 'DRAFT' before you "
                               "save the article as draft.")
                return render(request, self.template_name, self.context_object)

            if not request.user == old_article.author.username:
                messages.error(
                    request=self.request, message="You do not have permission to update this article.")
                return redirect(to="blog:written_articles")

            if article_update_form.is_valid():
                updated_article = article_update_form.save(commit=False)
                updated_article.author = request.user
                updated_article.date_published = None
                updated_article.date_updated = timezone.now()
                updated_article.save()
                article_update_form.save_m2m()

                messages.success(request, f"Article drafted successfully.")
                return redirect("blog:drafted_articles")

            self.context_object["article_update_form"] = article_update_form
            messages.error(request, "Please fill required fields")
            return render(request, self.template_name, self.context_object)

        if action == self.PUBLISH:

            if article_status == Article.DRAFTED:
                self.context_object["article_update_form"] = article_update_form

                messages.error(request,
                               "You clicked on 'PUBLISH' to publish the article"
                               " but selected the status as 'DRAFT'. "
                               "You can't Publish an article whose status is "
                               "'DRAFT'. Please change the status to "
                               "'PUBLISHED' before you can Publish the "
                               "article.")
                return render(request, self.template_name, self.context_object)

            if article_update_form.is_valid():

                updated_article = article_update_form.save(commit=False)
                updated_article.author = request.user
                updated_article.date_published = timezone.now()
                updated_article.date_updated = timezone.now()
                updated_article.save()
                article_update_form.save_m2m()

                messages.success(
                    self.request, f"Article updated successfully.")
                return redirect(to="blog:dashboard_article_detail", slug=updated_article.slug)

            self.context_object["article_update_form"] = article_update_form
            messages.error(request, "Please fill required fields")
            return render(request, self.template_name, self.context_object)


class ArticleDeleteView(LoginRequiredMixin, View):
    """
      Deletes article
    """

    def get(self, *args, **kwargs):
        """
           Checks if user who has requested to delete the article is the
           owner of the article.
           If the user is the owner, it sets the deleted field of the article to true and
           return a successful message.
           If the user is not the owner, it tells user he/she can't delete it
        """
        article = get_object_or_404(Article, slug=self.kwargs.get("slug"))

        if not self.request.user.username == article.author.username:
            messages.error(
                request=self.request, message="You do not have permission to delete this article.")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))

        article.deleted = True
        article.save()

        messages.success(request=self.request,
                         message="Article Deleted Successfully")
        return redirect(to='blog:deleted_articles')
