from django.contrib import admin
from bBlock.models import bBlock

class BlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'owner', 'create_timestamp', 'last_update_timestamp', )
    list_filter = ('owner', )

admin.site.register(bBlock, BlockAdmin)