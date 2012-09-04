# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelformset_factory
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from extra_views.formsets import ModelFormSetView
from skwissh.forms import ServerForm, ServerGroupForm, ProbeForm
from skwissh.models import Server, ServerGroup, Probe


#------------------------------------------------------------------------------
# Server
#------------------------------------------------------------------------------
class AddServerView(CreateView):
    model = Server
    form_class = ServerForm
    template_name = 'server-list.html'

    def get_success_url(self):
        return reverse_lazy('server-list')

    def get_context_data(self, **kwargs):
        context = super(AddServerView, self).get_context_data(**kwargs)
        ServerGroupFormSet = modelformset_factory(ServerGroup, form=ServerGroupForm)
        context['server_form'] = context['form']
        context['server_group_form'] = ServerGroupForm()
        context['server_group_formset'] = ServerGroupFormSet(queryset=ServerGroup.objects.all().select_related())
        context['groups'] = ServerGroup.objects.all().order_by('name')
        context['nogroup_servers'] = Server.objects.filter(servergroup__isnull=True).order_by('hostname')
        return context


class UpdateServerView(UpdateView):
    model = Server
    form_class = ServerForm
    template_name = 'server-detail.html'


class DeleteServerView(DeleteView):
    model = Server

    def get_success_url(self):
        return reverse_lazy('server-list')


#------------------------------------------------------------------------------
# Server Group
#------------------------------------------------------------------------------
class AddServerGroupView(CreateView):
    model = ServerGroup
    form_class = ServerGroupForm
    template_name = 'server-list.html'

    def get_success_url(self):
        return reverse_lazy('server-list')

    def get_context_data(self, **kwargs):
        context = super(AddServerGroupView, self).get_context_data(**kwargs)
        ServerGroupFormSet = modelformset_factory(ServerGroup, form=ServerGroupForm)
        context['server_form'] = ServerForm()
        context['server_group_form'] = context['form']
        context['server_group_formset'] = ServerGroupFormSet(queryset=ServerGroup.objects.all().select_related())
        context['groups'] = ServerGroup.objects.all().order_by('name')
        context['nogroup_servers'] = Server.objects.filter(servergroup__isnull=True).order_by('hostname')
        return context


class UpdateServerGroupView(ModelFormSetView):
    model = ServerGroup
    form_class = ServerGroupForm
    success_url = reverse_lazy('server-list')
    template_name = 'server-list.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateServerGroupView, self).get_context_data(**kwargs)
        context['server_form'] = ServerForm()
        context['server_group_form'] = ServerGroupForm()
        context['server_group_formset'] = context['formset']
        context['groups'] = ServerGroup.objects.all().order_by('name')
        context['nogroup_servers'] = Server.objects.filter(servergroup__isnull=True).order_by('hostname')
        return context


class DeleteGroupView(DeleteView):
    model = ServerGroup

    def get_success_url(self):
        return reverse_lazy('server-list')


#------------------------------------------------------------------------------
# Probes
#------------------------------------------------------------------------------
class AddProbeView(CreateView):
    model = Probe
    form_class = ProbeForm
    template_name = 'probe-list.html'

    def get_success_url(self):
        return reverse_lazy('probe-list')

    def get_context_data(self, **kwargs):
        context = super(AddProbeView, self).get_context_data(**kwargs)
        ProbeFormSet = modelformset_factory(Probe, form=ProbeForm)
        context['probe_form'] = context['form']
        context['probe_formset'] = ProbeFormSet(queryset=Probe.objects.all().select_related())
        context['probes'] = Probe.objects.all()
        context['groups'] = ServerGroup.objects.all().order_by('name')
        context['nogroup_servers'] = Server.objects.filter(servergroup__isnull=True).order_by('hostname')
        return context


class UpdateProbeView(ModelFormSetView):
    model = Probe
    form_class = ProbeForm
    success_url = reverse_lazy('probe-list')
    template_name = 'probe-list.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateProbeView, self).get_context_data(**kwargs)
        context['probe_form'] = ProbeForm()
        context['probe_formset'] = context['formset']
        context['probes'] = Probe.objects.all()
        context['groups'] = ServerGroup.objects.all().order_by('name')
        context['nogroup_servers'] = Server.objects.filter(servergroup__isnull=True).order_by('hostname')
        return context


class DeleteProbeView(DeleteView):
    model = Probe

    def get_success_url(self):
        return reverse_lazy('probe-list')
