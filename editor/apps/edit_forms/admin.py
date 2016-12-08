from django.contrib import admin

from .models import *

class EditFieldInline(admin.TabularInline):
    model = EditField

class EditFormAdmin(admin.ModelAdmin):
    inlines = (EditFieldInline,)

class FormEditFieldInline(admin.TabularInline):
    model = EditForm.form_fields.through
    inlines = (EditFieldInline,)
    extra = 0 

class EditFormAdmin(admin.ModelAdmin):
    inlines = (FormEditFieldInline,)
    exclude = ('form_fields',)

admin.site.register(EditForm, EditFormAdmin)
admin.site.register(EditField, EditFormAdmin)
