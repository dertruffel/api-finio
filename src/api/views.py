import datetime
import json
import math
import secrets
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions, exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.calculator import Calculator
from api.models import NewsObject
from api.serializers.serializers import CalculatorPaySerializer, ArticleSerializer
from config.celery_helper import CeleryHelper


class CalculatorPay(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CalculatorPaySerializer
    http_method_names = ['post']

    @extend_schema(
        methods=['POST'],
        summary='CalculatorPay',
        description='''CalculatorPay \n
            ''',
    )
    def post(self, request):
        try:
            calc = Calculator()
            data = request.data
            serializer = CalculatorPaySerializer(data=data)
            if serializer.is_valid():
                data = serializer.data
                print("data", data)
                if data['type']=='uop':
                    result = calc.uop(data)
                elif data['type']=='b2b':
                    result = calc.b2b(data)
                elif data['type']=='uz':
                    result = calc.uz(data)
                elif data['type']=='ud':
                    result = calc.uod(data)
                else:
                    raise exceptions.ValidationError('Wrong type')
                print("result", result)
            return Response(result)
        except Exception as e:
            print(e)
            raise exceptions.ValidationError('Wrong data')


class Articles(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ArticleSerializer
    http_method_names = ['get']

    @extend_schema(
        methods=['GET'],
        summary='Articles',
        description='''Articles \n
            ''',
    )
    def get(self, request, ):
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        page = int(page)
        page_size = int(page_size)
        articles = NewsObject.objects.all().order_by('-created_at')
        total = articles.count()
        pages = math.ceil(total / page_size)
        articles = articles[(page - 1) * page_size:page * page_size]
        serializer = ArticleSerializer(articles, many=True)
        return Response({
            'total': total,
            'pages': pages,
            'page': page,
            'page_size': page_size,
            'articles': serializer.data
        })
