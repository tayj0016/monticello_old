from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
        #index homepage, generic class-based
        path('', views.IndexView.as_view(), name='index'),

        # Recipe details
        path('<int:pk>/', views.RecipeView.as_view(), name='detail'),

        # Create a new recipe, function-based
        path('new/', views.recipe_new, name='recipe_new'),

        # Add comment to recipe
        path('<int:pk>/comment', views.CommentView.as_view(), name='comment'),

        # Update a recipe, generic class-based
        path('<int:pk>/update', views.UpdateView.as_view(), name='update'),

        # delete a recipe, generic class-based
        path('<int:pk>/delete', views.RecipeDelete.as_view(), name='delete'),
]