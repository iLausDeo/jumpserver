# -*- coding: utf-8 -*-
#

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed

from common.mixins.api import CommonApiMixin
from common.permissions import IsValidUser, IsOrgAdmin
from common.const.http import POST, PUT
from tickets import serializers, const
from tickets.permissions.ticket import IsAssignee, NotClosed
from tickets.models import Ticket


__all__ = ['TicketViewSet']


class TicketViewSet(CommonApiMixin, viewsets.ModelViewSet):
    permission_classes = (IsValidUser,)
    serializer_class = serializers.TicketSerializer
    serializer_classes = {
        'default': serializers.TicketDisplaySerializer,
        'display': serializers.TicketDisplaySerializer,
        'open': serializers.TicketApplySerializer,
        'approve': serializers.TicketApproveSerializer,
        'reject': serializers.TicketRejectSerializer,
        'close': serializers.TicketCloseSerializer,
    }
    filter_fields = [
        'id', 'title', 'type', 'action', 'status', 'applicant', 'applicant_display', 'processor',
        'processor_display', 'assignees__id'
    ]
    search_fields = [
        'title', 'action', 'type', 'status', 'applicant_display', 'processor_display'
    ]

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(self.action)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(self.action)

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(self.action)

    def get_queryset(self):
        queryset = Ticket.get_user_related_tickets(self.request.user)
        return queryset

    @action(detail=False, methods=[POST])
    def open(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=[PUT], permission_classes=[IsOrgAdmin, IsAssignee, NotClosed])
    def approve(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=[PUT], permission_classes=[IsOrgAdmin, IsAssignee, NotClosed])
    def reject(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=[PUT], permission_classes=[IsOrgAdmin, IsAssignee, NotClosed])
    def close(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_dynamic_mapping_fields_mapping_rule(self):
        from tickets.serializers.ticket.meta import get_meta_field_mapping_rule_by_view
        meta_field_mapping_rule = get_meta_field_mapping_rule_by_view(self)
        fields_mapping_rule = {
            'meta': meta_field_mapping_rule,
        }
        return fields_mapping_rule