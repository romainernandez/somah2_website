from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic import DeleteView

from home.forms import EditPeriodExtendedMultiForm, AddPeriodForm
from home.models import Period, Language, PeriodTr, Topic, TopicTr, Content, ContentTr
from somah2_website.local_settings import TRELLO_API_KEY


def dashboard(request):
    return render(request, 'home/dashboard.html', { 'TRELLO_API_KEY':TRELLO_API_KEY })


def view_period(request, period_id):
    try:
        period = Period.objects.get(id=period_id)
    except Exception as e:
        raise Http404
    else:
        return HttpResponse("period: " + str(period.id))


def user(request):
    return render(request, template_name='home/user.html')


def notifications(request):
    return render(request, template_name='home/notifications.html')


def table(request):
    all_languages = Language.objects.all().order_by('country') # country_code
    all_flags = list()
    for language in all_languages:
        all_flags.append(language.country.flag)

    all_periods = Period.objects.all()
    all_periods_trs = list() # [periods_trs_for_period1, periods_trs_for_period2..]
    for period in all_periods:
        all_periods_trs.append(PeriodTr.objects.filter(period=period).order_by('language__country')) # list
    all_periods_extended = zip(all_periods, all_periods_trs)

    all_topics = Topic.objects.all()
    all_topics_trs = list() # [topics_trs_for_topic1, topics_trs_for_topic2..]
    for topic in all_topics:
        all_topics_trs.append(TopicTr.objects.filter(topic=topic).order_by('language__country')) # list
    all_topics_extended = zip(all_topics, all_topics_trs)

    all_contents = Content.objects.all()
    all_contents_trs = list()
    for content in all_contents:
        all_contents_trs.append(ContentTr.objects.filter(content=content).order_by('language__country'))  # list
    all_contents_extended = zip(all_contents, all_contents_trs)

    return render(request, 'home/table.html', { 'all_flags':all_flags, 'all_periods_extended':all_periods_extended,
            'all_topics_extended':all_topics_extended, 'all_contents_extended':all_contents_extended })


def remove_period_extended(request, period_id):
    Period.objects.filter(id=period_id).delete()
    return redirect('table')


class EditPeriodExtendedView(UpdateView):
    model = PeriodTr
    form_class = EditPeriodExtendedMultiForm
    template_name = 'home/edit_period_extended.html'
    success_url = reverse_lazy('edit_period_extended_success')

    def get_object(self, queryset=None):
        period_id = self.kwargs.get('period_id')
        country_code = self.kwargs.get('language')
        language = Language.objects.get(country=country_code)
        return PeriodTr.objects.get(period__id=period_id, language=language)

    def get_form_kwargs(self):
        kwargs = super(EditPeriodExtendedView, self).get_form_kwargs()
        kwargs.update(instance={
            'period': self.object.period,
            'period_tr': self.object,
        })
        return kwargs

class AddPeriodExtendedView(CreateView):
    model = Period
    form_class = AddPeriodForm
    template_name = 'home/add_period_extended.html'

    def form_valid(self, form):
        form.save()
        id = form['id'].value()
        period = Period.objects.get(id=id)
        all_languages = Language.objects.all().order_by('country')  # country_code
        for language in all_languages:
            period_tr = PeriodTr.objects.create(language=language, period=period)
        return redirect('add_period_extended_success')