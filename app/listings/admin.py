from django.contrib import admin

from .models import Listing

class ListingAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'is_published', 'price', 'list_date', 'oldpartnerlisting', 'marketbias', 'promotion')
  #list_display = ('id', 'title', 'is_published', 'price', 'list_date', 'oldpartnerlisting', 'market_bias')
  list_display_links = ('id', 'title')
  list_filter = ('oldpartnerlisting',)
  list_editable = ('is_published',)
  #search_fields = ('title', 'description', 'address', 'city', 'state', 'zipcode', 'price')
  search_fields = ('title', 'description', 'price', 'marketbias')
  list_per_page = 25

#admin.site.register(Listing, ListingAdmin)
admin.site.register(Listing)