from django.contrib import admin
from user import models


class UserScoreAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'types', 'points')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class UserScoreTransactionAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(models.User)
admin.site.register(models.UserAddress)
admin.site.register(models.UserScoreTransaction, UserScoreTransactionAdmin)
admin.site.register(models.UserScore, UserScoreAdmin)
