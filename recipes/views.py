from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bs4 import BeautifulSoup
from django.views import View
from .forms import RecipeForm, CommentForm
from .models import Recipe, Comment, Category

import requests


# Generic class-based view for index
# Uses recipe_list.html as default template, unless otherwise specified
class IndexView(ListView):
    # template_name = 'recipes/recipe_index.html'
    queryset = Recipe.objects.order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Generic class-based view for displaying recipe details
class RecipeView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'

    def get_object(self, **kwargs):
        return get_object_or_404(Recipe, pk=self.kwargs['pk'])

    def get_queryset(self):
        return Recipe.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(recipe=self.kwargs['pk']).order_by('created_at')
        context['category_list'] = Category.objects.all()
        return context


# function-based view for creating a new recipe using forms
# Check form action attr and header navbar
@login_required
def recipe_new(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            URL = form.cleaned_data['url']
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            thumb = soup.find("meta", property="og:image")
            title = soup.find("meta", property="og:title")
            website = soup.find("meta", property="og:site_name")
            website_url = soup.find("meta", property="og:url")
            description = soup.find("meta", property="og:description")
            recipe.title = title["content"]
            recipe.thumb = thumb["content"]
            recipe.description = description["content"]
            recipe.website = website["content"]
            recipe.website_url = website_url["content"].rsplit(".com")[0] + ".com"
            recipe.author = request.user
            recipe.save()
            return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})


# class-based view for adding comments
@method_decorator(login_required, name='dispatch')
class CommentView(FormView):
    template_name = 'recipes/comment_form.html'
    form_class = CommentForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        comment = form.save(commit=False)
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        comment.recipe = recipe
        comment.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        pk = self.kwargs['pk']
        return reverse_lazy('recipes:detail', kwargs={'pk': pk})


@method_decorator(login_required, name='dispatch')
class UpdateView(UpdateView):
    model = Recipe
    template_name = 'recipes/recipe_edit.html'
    fields = ['title', 'url', 'website']


# Generic class-based view for deleting a recipe
@method_decorator(login_required, name='dispatch')
class RecipeDelete(DeleteView):
    # template_name = 'recipes/recipe_delete.html'
    model = Recipe
    success_url = reverse_lazy('recipes:index')
