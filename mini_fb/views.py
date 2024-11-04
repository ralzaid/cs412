from django.shortcuts import render, redirect

from .models import * 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.urls import reverse
from .models import Profile, StatusMessage, Image
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        login(self.request, user)
        form.instance.user = user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile
        response = super().form_valid(form)

        image_file = form.cleaned_data.get('image_file')
        if image_file:
            Image.objects.create(
                image_file=image_file,
                status_message=self.object,
            )

        return response

    def get_success_url(self):
        profile = Profile.objects.get(user=self.request.user)
        return reverse('show_profile', kwargs={'pk': profile.pk})

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
    def get_object(self):
        profile = Profile.objects.get(user=self.request.user)
        return profile



class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    

class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        other = Profile.objects.get(pk=self.kwargs['other_pk'])
        profile.add_friend(other)
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['suggested_friends'] = profile.get_friend_suggestions()

        return context
    
    def get_object(self):
        profile = Profile.objects.get(user=self.request.user)
        return profile

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['news_feed'] = self.object.get_news_feed()
    #     return context
    
    def get_object(self):
            profile = Profile.objects.get(user=self.request.user)
            return profile
    





    