from notes.models import Note, NoteItem
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.http import HttpResponse


class NoteCreateMixin:
    app_label = None
    model = None
    template_name = None

    def get(self, request, id):
        content_type = ContentType.objects.get_by_natural_key(app_label=self.app_label, model=self.model)
        added_notes = Note.objects.filter(note_item__content_type=content_type, note_item__object_id=id)
        notes = Note.objects.all().exclude(note_item__content_type=content_type, note_item__object_id=id)
        return render(request, self.template_name, context={"notes": notes, "added_notes": added_notes})

    def post(self, request, id):
        content_type = ContentType.objects.get_by_natural_key(app_label=self.app_label, model=self.model)
        note_name = request.POST["note"]
        note = Note.objects.get(name=note_name)
        NoteItem.objects.create(content_type=content_type, object_id=id, note=note)
        return HttpResponse("OK")
