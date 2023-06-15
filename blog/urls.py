
# Core Django imports.
from django.urls import path
# Blog application imports.
from blog.views import (
    ArticleListView,
    ArticleDetailView,
    ArticleSearchListView,
    TagArticlesListView,
)
from blog.views import (
    CategoryArticlesListView,
    CategoriesListView,
    CategoryCreateView,
    CategoryUpdateCreateView,
)

# from blog.views import (
#     AuthorArticlesListView,
#     AuthorsListView,
# )

from blog.views import (
    CommentCreateView,
    ArticleCommentList
)
from blog.views import (
    ArticleWriteView,
    ArticleUpdateView,
    ArticleDeleteView,
)

# from blog.views import (
#     AuthorProfileUpdateView,
#     AuthorProfileView,
# )

# from blog.views import \
#     (
#         ActivateView,
#         AccountActivationSentView,
#         UserRegisterView,
#     )
# from blog.views import UserLogoutView
# from blog.views import UserLoginView
# Specifies the app name for name spacing.
app_name = "blog"
# article/urls.py
urlpatterns = [
    # ARTICLE URLS #
    # /home/
    path(
        route='',
        view=ArticleListView.as_view(),
        name='home'
    ),
    # /article/<str:slug>/
    path(
        route='<str:slug>/',
        view=ArticleDetailView.as_view(),
        name='article_detail'
    ),
    # /search/?q=query/
    path(
        route='article/search/',
        view=ArticleSearchListView.as_view(),
        name='article_search_list_view'
    ),
    # /tag/<str:tag_name>/
    path(
        route='tag/<str:tag_name>/articles',
        view=TagArticlesListView.as_view(),
        name="tag_articles"
    ),

    # AUTHORS URLS #

    # /authors-list/
    # path(
    #     route='authors/list/',
    #     view=AuthorsListView.as_view(),
    #     name='authors_list'
    # ),

    # # /author/<str:username>/
    # path(
    #     route='author/<str:username>/articles',
    #     view=AuthorArticlesListView.as_view(),
    #     name='author_articles'
    # ),

    # CATEGORY URLS #
    # category-articles/<str:slug>/
    path(
        route='category/<str:slug>/articles',
        view=CategoryArticlesListView.as_view(),
        name='category_articles'
    ),
    # /categories-list/
    path(
        route='categories/list/',
        view=CategoriesListView.as_view(),
        name='categories_list'
    ),
    # /category/new/
    path(
        route='category/create/',
        view=CategoryCreateView.as_view(),
        name="category_create"
    ),
    # /category/<str:slug>/update/
    path(
        route='category/<str:slug>/update/',
        view=CategoryUpdateCreateView.as_view(),
        name="category_update"
    ),
    # me/article/write
    path(
        route='me/article/write/',
        view=ArticleWriteView.as_view(),
        name="article_write"
    ),
    # me/article/<str:slug>/update/
    path(
        route='me/article/<str:slug>/update/',
        view=ArticleUpdateView.as_view(),
        name="article_update"
    ),
    # /article/<str:slug>/delete/
    path(
        route='me/article/<str:slug>/delete/',
        view=ArticleDeleteView.as_view(),
        name="article_delete"
    ),
    # COMMENT URLS #
    # /comment/new/
    path(
        route='comment/new/<str:slug>/',
        view=CommentCreateView.as_view(),
        name="comment_create"
    ),
    # /<str:slug>/comments/
    path(
        route='<str:slug>/comments/',
        view=ArticleCommentList.as_view(),
        name="article_comments"
    ),
]
