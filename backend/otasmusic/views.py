from django.core.paginator import Paginator
from django.db.models.aggregates import Count
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.detail import DetailView
from otasmusic.models import Song, Person, AuthorLyrics, AuthorMusic, RecordContributor, Record, Band, Event, Album
from django.contrib.auth.mixins import LoginRequiredMixin
from otasmusic.forms.UserSignUpForm import UserSignUpForm
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class HomePageView(TemplateView):
  template_name = "views/homepage_view.html"

  def get_context_data(self, **kwargs):
    context = super(HomePageView, self).get_context_data(**kwargs)
    context["record_list"] = Record.objects.select_related("song", "band", "album")
    # context["event_list"] = Event.objects.all()[:3]
    context["record_count"] = Record.objects.count()
    context["person_count"] = Person.objects.count()
    return context


class RecentView(TemplateView):
  NUM_RECORDS_PER_REQUEST = 3

  template_name = "views/recent_view.html"

  def get_context_data(self, **kwargs):
    context = super(RecentView, self).get_context_data(**kwargs)
    page = self.request.GET.get('page', 1)
    record_list = Record.objects.all()
    record_paginator = Paginator(record_list, self.NUM_RECORDS_PER_REQUEST)
    context["record_list"] = record_paginator.page(page)
    return context


class BandDetailView(DetailView):
  template_name = "views/band_view.html"
  context_object_name = "band"

  def get_queryset(self):
    return (
      Band.objects.get_queryset()
      .prefetch_related("bandcontact_set", "record_set__song", "album_set")
    )


class SongDetailView(DetailView):
  template_name = "views/song_view.html"
  context_object_name = "song"

  def get_queryset(self):
    return (
      Song.objects.get_queryset()
      .select_related("band")
      .prefetch_related("authorlyrics_set__person",
                        "authormusic_set__person",
                        "record_set__recordcontributor_set__recordcontributorskill_set__skill",
                        "record_set__recordcontributor_set__person",
                        )
    )


class RecordListView(ListView):
  template_name = "views/record_list_view.html"
  model = Record
  context_object_name = "record_list"

  def get_ordering(self):
    ordering = self.request.GET.get('ordering', self.model._meta.ordering)
    if ordering in ["song__name"]:
      return ordering
    return self.ordering


# @method_decorator(cache_page(60 * 60 * 24 * 3, cache='view'), name='dispatch')
class RecordDetailView(DetailView):
  template_name = "views/record_view.html"
  context_object_name = "record"

  def get_queryset(self):
    return (
      Record.objects
      .get_queryset()
      .select_related("song", "band", "album")
      .prefetch_related("song__authorlyrics_set__person",
                        "song__authormusic_set__person",
                        "recordcontributor_set__person",
                        "recordcontributor_set__recordcontributorskill_set__skill")
    )


class PersonListView(LoginRequiredMixin, ListView):
  template_name = "views/person_list_view.html"
  model = Person
  context_object_name = "person_list"

  def get_queryset(self):
    return Person.objects \
      .annotate(num_author_lyrics=Count('authorlyrics', distinct=True)) \
      .annotate(num_author_music=Count('authormusic', distinct=True)) \
      .annotate(num_record_contributor=Count('recordcontributor', distinct=True)) \
      .order_by('-num_record_contributor', '-num_author_lyrics', '-num_author_music')


class PersonDetailView(DetailView):
  template_name = "views/person_view.html"
  model = Person
  context_object_name = "person"

  def get_context_data(self, **kwargs):
    context = super(PersonDetailView, self).get_context_data(**kwargs)
    person = context[self.context_object_name]
    context['author_lyrics'] = (
      AuthorLyrics.objects
      .filter(person=person)
      .select_related("song")
      .order_by("song__name")
    )

    context['author_music'] = (
      AuthorMusic.objects
      .filter(person=person)
      .select_related("song")
      .order_by("song__name")
    )

    context['record_contributors'] = (
      RecordContributor.objects
      .select_related("record__song__band", "person")
      .prefetch_related("recordcontributorskill_set__skill")
      .filter(person=person)
      .order_by("-record__release_date")
    )
    return context

  def get_queryset(self):
    return (
      Person.objects
      .get_queryset()
      .prefetch_related("personcontact_set")
    )


class EventDetailView(DetailView):
  template_name = "views/event_view.html"
  model = Event
  context_object_name = "event"


class AlbumDetailView(DetailView):
  template_name = "views/album_view.html"
  model = Album
  context_object_name = "album"


class UserSignUpView(FormView):
  template_name = "registration/user_sign_up_form.html"
  form_class = UserSignUpForm
  success_url = '/'  # TODO stranka s navodem

  def form_valid(self, form):
    form.save()

    return super(UserSignUpView, self).form_valid(form)


class ServicesView(TemplateView):
  template_name = "views/services_view.html"


class ContactView(TemplateView):
  template_name = "views/contact_view.html"


class CalendarView(TemplateView):
  template_name = "views/calendar_view.html"
