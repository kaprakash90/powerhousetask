from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404
from .models import TreeAPI, Tree
import json

@csrf_exempt
def pruned_list(request, name):
  indicator_ids = request.GET.getlist('indicator_ids[]')
  indicator_ids = list(map(int, indicator_ids))
  if not indicator_ids:
    return JsonResponse({'error': "check your input"}, status=404)
  try:
    json_data = TreeAPI(name).get()
  except Http404:
    return JsonResponse({'error': "Requested tree source is not available"}, status=404)
  except Exception:
    return JsonResponse({"error": "The API is not alright"}, status=500)
  tree = Tree(json_data)
  tree.prune(indicator_ids)
  return JsonResponse(tree.to_json()['themes'], safe=False)
