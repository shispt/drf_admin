""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : views.py 
@create   : 2020/7/1 22:37 
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class MultipleDestroyMixin:
    """
    自定义批量删除mixin
    """

    def multiple_delete(self, request, *args, **kwargs):
        delete_ids = request.data.get('ids')
        if not delete_ids:
            return Response(data={'detail': '参数错误,ids为必传参数'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(delete_ids, list):
            return Response(data={'detail': 'ids格式错误,必须为List'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        del_queryset = queryset.filter(id__in=delete_ids)
        if len(delete_ids) != len(del_queryset):
            return Response(data={'detail': '删除数据不存在'}, status=status.HTTP_400_BAD_REQUEST)
        for queryset in del_queryset:
            queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminViewSet(ModelViewSet, MultipleDestroyMixin):
    """
    继承ModelViewSet, 并新增MultipleDestroyMixin
    添加multiple_delete action
    """
    pass
