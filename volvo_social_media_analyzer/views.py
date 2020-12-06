from django.http import HttpResponse  # 导入HttpResponse模块
from django.views import View

import handler.account_page_handler as accountH
import handler.mention_page_handler as mentionH


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello world! This is get.")


class AccountPageView(View):
    def get(self, request, *args, **kwargs):
        response = accountH.get_account_response(int(request.GET.get("duration_mode")))
        return HttpResponse(response)


class MentionPageView(View):
    def get(self, request, *args, **kwargs):
        response = mentionH.get_mention_response()
        return HttpResponse(response)
