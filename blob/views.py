from django.http.response import JsonResponse
from blob.models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json

def build_tree_structure(nodes, parent=None):
    tree_data = []

    for node in nodes.filter(related=parent):
        node_dict = {
            'id': node.id,
            'name': node.name,
            'related': build_tree_structure(nodes, parent=node)
        }
        tree_data.append(node_dict)

    return tree_data


def get_sectors(request):
    data = build_tree_structure(Sector.objects)
    return JsonResponse(data, safe=False)


def get_data(request):
    data = None
    try:
        data = Form.objects.filter(session__id=request.META['HTTP_SESSION_ID']).select_related('sector').values('id','name', 'sector__name')
        return JsonResponse(list(data), safe=False)
    except:
        print(data)
        return JsonResponse([], safe=False)

@csrf_exempt
def update_form(request, id):
    if request.method == "GET":
        try:
            data = Form.objects.filter(id=id).select_related('sector').values('id','name', 'sector__name', 'sector__id')
            return JsonResponse(list(data)[0], safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"type": "error", "message": "ID doesn't exist"})
    try:
        data = json.loads(request.body)
        form = Form.objects.filter(id=id)
        if not form.exists():
            return JsonResponse({"type": "error", "message": "ID doesn't exist"})
        form = form.get()
        form.name = data['name']
        form.sector_id = data['sector']['id']
        form.save()
        return JsonResponse({"type": "success", "message": "Data updated"})
    except Exception as e:
        return JsonResponse({"type": "error", "message": "Something went wrong try again"})



def create_session(request):
    s = Session.objects.create()
    return JsonResponse({"id":s.id})

@csrf_exempt
def create_form(request):
    data = json.loads(request.body)
    try:
        form = Form.objects.create(
            session_id=request.META['HTTP_SESSION_ID'],
            name=data['name'],
            sector_id=data["sector"]["id"]
        )
        return JsonResponse({"type":"sucess", "message":"Data was saved"})
    except Exception as e:
        print(e)
        return JsonResponse({"type":"error", "message":"Pls complete missing data"})
