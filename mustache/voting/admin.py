from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from voting.models import Gentleman,Vote

class GentlemanInline(admin.StackedInline):
	model = Gentleman
	can_delete = False
    
class VoteInline(admin.StackedInline):
    model = Vote
    can_delete = False
	
class UserAdmin(UserAdmin):
	inlines = (GentlemanInline,VoteInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Gentleman)
admin.site.register(Vote)
