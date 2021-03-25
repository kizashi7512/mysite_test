# from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from thread.models import Vote

class CreateVoteView(View):
  '''
  いいね投稿作成処理を行う
  '''
  def post(self, request, *args, **kwargs):
    res = {
      'result':False,
      'message':'処理に失敗しました。'
    }
    if not 'comment_id' in request.POST:
      return JsonResponse(res, status=400)

    comment_id = request.POST['comment_id']
    ip_address = get_cliend_ip(request)

    if Vote.objects.filter(comment_id=comment_id,ip_address=ip_address):
      res['message'] = '投稿済みです'
      return JsonResponse(res, staus=409)

    if Vote.objects.create_vote(ip_address, comment_id):
      res['result'] = True
      res['message'] = 'ポイントを追加しました'
      return JsonResponse(res, status=201)
    else: 
      return JsonResponse(res,statis=500)

def get_cliend_ip(request):
  '''
  IPアドレスを取得する
  '''
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.spliot(',')[0]
  else:
    ip =request.META.get('REMOTE_ADDR')
  return ip


# Create your views here.
