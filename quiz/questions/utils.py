from django.shortcuts import render, redirect
from .forms import *


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, {'form': form})

    def post(self, request):
        bound_form = self.form_model(request.POST)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        else:
            return render(request, self.template, {'form': bound_form, "errors": bound_form.errors})


class ObjectUpdateMixin:
    model = None
    form_model = None
    template = None

    def get(self, request, id):
        obj = self.model.objects.get(id=id)
        form = self.form_model(instance=obj)
        return render(request, self.template, {'obj': obj, 'form': form})

    def post(self, request, id):
        if "update" in request.POST:

            obj = self.model.objects.get(id=id)
            bound_form = self.form_model(request.POST, instance=obj)

            if bound_form.is_valid():
                update_obj = bound_form.save()
                return redirect(update_obj)
            else:
                return render(request, self.template, {'obj': obj,
                                                       'form': bound_form,
                                                       "errors": bound_form.errors})

        elif "delete" in request.POST:
            obj = self.model.objects.get(id=id)
            obj.delete()
            return redirect(obj)
