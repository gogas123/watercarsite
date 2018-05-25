from django.contrib import admin
from waterapp.models import Constructionpost,TOS



admin.site.register(Constructionpost) # 기본 ModelAdmin으로 등록
admin.site.register(TOS)

