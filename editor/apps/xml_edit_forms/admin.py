from django.contrib import admin

from .models import *

class XMLEditFieldInline(admin.TabularInline):
    model = XMLEditField
    extra = 0

class XMLEditFieldRelationshipInline(admin.TabularInline):
    model = XMLEditForm.form_fields.through
    inlines = (XMLEditFieldInline,) 
    extra = 0

class XMLEditFormAdmin(admin.ModelAdmin):
    inlines = (XMLEditFieldRelationshipInline,)

admin.site.register(XMLEditForm, XMLEditFormAdmin)
admin.site.register(XMLEditField)
