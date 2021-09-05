from django.http import JsonResponse
from django.views.generic import DetailView
from django.views.generic.list import BaseListView
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from movies.models import FilmWork


class FilmWorkApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        return FilmWork.objects.values(

        ).annotate(
            genres=ArrayAgg(
                'genres__name'
            )
        ).annotate(
            writers=ArrayAgg(
                'filmworkperson__person__full_name',
                filter=Q(
                    filmworkperson__role='writer'
                )
            )
        ).annotate(
            actors=ArrayAgg(
                'filmworkperson__person__full_name',
                filter=Q(
                    filmworkperson__role='actor'
                )
            )
        ).annotate(
            directors=ArrayAgg(
                'filmworkperson__person__full_name',
                filter=Q(
                    filmworkperson__role='director'
                )
            )
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class FilmWorkApi(FilmWorkApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        data = self.get_queryset()

        paginator, page, object_list, is_paginated = self.paginate_queryset(data, self.paginate_by)
        count = paginator.count
        total_pages = paginator.num_pages
        prev = page.previous_page_number() if page.has_previous() else None
        next = page.next_page_number() if page.has_next() else None

        context = {
            'count': count,
            'total_pages': total_pages,
            'prev': prev,
            'next': next,
            'results': list(object_list)
        }
        return context


class FilmWorkDetailsApi(FilmWorkApiMixin, DetailView):

    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_object()
