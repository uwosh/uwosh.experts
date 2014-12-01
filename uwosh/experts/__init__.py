from uwosh.experts import content
from Products.Archetypes import atapi
from Products.CMFCore import utils as cmfutils
ADD_CONTENT_PERMISSION = "uwosh.experts: Add Expert"

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    import content

    content_types, constructors, ftis = atapi.process_types(atapi.listTypes('uwosh.experts'), 'uwosh.experts')

    cmfutils.ContentInit(
        'uwosh.experts Content',
        content_types = content_types,
        permission = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti = ftis,
        ).initialize(context)

