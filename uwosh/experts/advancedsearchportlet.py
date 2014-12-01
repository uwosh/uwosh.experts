from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from plone.memoize.instance import memoize
from Acquisition import aq_inner
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from zope.component import getMultiAdapter

from plone.app.portlets.portlets import search

class IAdvancedSearchPortlet(search.ISearchPortlet):
    """ A portlet displaying a (live) search box
    """

    searchTitle = schema.ASCIILine(
        title = _(u"Search Title"),
        description = _(u"Sets the title of the search box."),
        required = True,
        default = "Search"
    )
            
    objectToSearch = schema.Choice(
        title=_(u"Target area to search"),
        description=_(u"Find the content item in which you only want to search in"),
        required=True,
        source=SearchableTextSourceBinder({}, default_query='path:')
    )

class Assignment(search.Assignment):
    implements(IAdvancedSearchPortlet)

    def __init__(self, enableLivesearch=True, objectToSearch=None, searchTitle="Search"):
        self.enableLivesearch=enableLivesearch
        self.objectToSearch = objectToSearch
        self.searchTitle = searchTitle

class Renderer(search.Renderer):

    render = ViewPageTemplateFile('advancedsearchportlet.pt')

    def search_in_section_only(self):
        return self.object_to_search_in_path() is not None

    def title(self):
        return self.data.searchTitle

    @memoize
    def object_to_search_in_path(self):
        path = self.data.objectToSearch
        if not path:
            return None
            
        if path.startswith("/"):
            path = path[1:]
            
        if not path:
            return None
            
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        return portal.restrictedTraverse(path, default=None).getPhysicalPath()

class AddForm(search.AddForm):
    form_fields = form.Fields(IAdvancedSearchPortlet)
    form_fields['objectToSearch'].custom_widget = UberSelectionWidget
    
    label = _(u"Add Search Portlet")
    description = _(u"This portlet shows a search box.")

    def create(self, data):
        return Assignment()


class EditForm(search.EditForm):
    form_fields = form.Fields(IAdvancedSearchPortlet)
    form_fields['objectToSearch'].custom_widget = UberSelectionWidget
    
    label = _(u"Edit Search Portlet")
    description = _(u"This portlet shows a search box.")
