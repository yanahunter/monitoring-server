import base64
from io import BytesIO

from django.views.generic import TemplateView
from rest_framework.generics import CreateAPIView

from core.models import Report
from core.serializers import ReportSerializer
from matplotlib import pyplot as plt


class ReportView(CreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


class ComputersTemplateVew(TemplateView):
    template_name = 'computers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['computers'] = Report.objects.all().distinct('computer_id')
        return context


class HistogramsTemplateView(TemplateView):
    template_name = 'histograms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        computer_id = kwargs.get('computer_id')
        reports_queryset = Report.objects.filter(computer_id=computer_id)

        cpu_percent_to_date_timing = self.get_mapping(reports_queryset, 'cpu_percent')
        context['cpu_percent_hist'] = self.get_hist(cpu_percent_to_date_timing)

        free_ram_to_date_timing = self.get_mapping(reports_queryset, 'free_ram')
        context['free_ram_hist'] = self.get_hist(free_ram_to_date_timing)

        free_disk_space_to_date_timing = self.get_mapping(reports_queryset, 'free_disk_space')
        context['free_disk_space_hist'] = self.get_hist(free_disk_space_to_date_timing)

        processes_count_to_date_timing = self.get_mapping(reports_queryset, 'processes_count')
        context['processes_count_hist'] = self.get_hist(processes_count_to_date_timing)

        return context

    def get_hist(self, mapping):
        image = BytesIO()
        plt.bar(mapping.keys(), mapping.values(), width=0.1)
        plt.savefig(image, format='png')
        plt.cla()
        return base64.b64encode(image.getvalue()).decode('ascii')

    def get_mapping(self, reports_queryset, field):
        reports_list = list(reports_queryset.values('date', field))
        date_to_field_map = {
            str(report_data.get('date').strftime("%Y-%m-%d %H:%M:%S")): report_data.get(field)
            for report_data in reports_list if report_data.get(field) is not None
        }
        return date_to_field_map
