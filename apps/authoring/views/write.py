from annoying.decorators import JsonResponse
from authoring.models import AuthoredMaterial
from authoring.views import EditMaterialViewMixin
from django import forms
from django.contrib import messages
from django.shortcuts import  redirect
from django.views.generic import UpdateView


class WriteForm(forms.ModelForm):

    # TODO: clean up HTML from `text` field.
    # using lxml clean. Remove all styles, Keep only allowed classes,
    # remove scripts, styles, forms, iframes, objects, embeds

    class Meta:
        model = AuthoredMaterial
        fields = ["title", "text"]
        widgets = dict(
            title=forms.HiddenInput(),
            text=forms.Textarea(),
        )


class Write(EditMaterialViewMixin, UpdateView):

    template_name = "authoring/write.html"
    form_class = WriteForm

    def form_valid(self, form):
        form.save()
        if self.request.is_ajax():
            return JsonResponse(dict(
                status="success",
                message=u"Saved.",
            ))
        if self.request.POST.get("next") == "true":
            return redirect("authoring:describe", pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        if self.request.is_ajax():
            errors = {}
            for field, errors_list in form.errors.items():
                errors[field] = errors_list[0]
            return JsonResponse(dict(
                status="error",
                message=u"Please correct the indicated errors.",
                errors=errors,
            ))
        messages.error(self.request, u"Please correct the indicated errors.")
        return self.render_to_response(self.get_context_data(form=form))
