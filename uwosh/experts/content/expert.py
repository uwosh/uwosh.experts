

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.validation import V_REQUIRED
from Products.ATContentTypes.configuration import zconf

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from uwosh.experts.config import *
from Products.ATContentTypes.content.document import ATDocumentBase
from Products.ATContentTypes.lib.imagetransform import ATCTImageTransform

copied_fields = {}
copied_fields['title'] = BaseSchema['title'].copy()
copied_fields['title'].searchable = True
copied_fields['title'].widget.label = "Name"
schema = Schema((

    copied_fields['title'],

    StringField(
        name='department',
        widget=StringField._properties['widget'](
            label="Department",
        ),
        searchable=True,
    ),
    StringField(
        name='professionalTitle',
        widget=StringField._properties['widget'](
            label='Title',
        ),
        searchable=True,
    ),
    StringField(
        name='workPhone',
        widget=StringField._properties['widget'](
            label='Work Phone'
        ),
        searchable=True,
    ),
    StringField(
        name='homePhone',
        widget=StringField._properties['widget'](
            label='Home Phone'
        ),
        searchable=True,
    ),
    StringField(
        name='mobilePhone',
        widget=StringField._properties['widget'](
            label='Mobile Phone',
        ),
        searchable=True,
    ),
    StringField(
        name='email',
        widget=StringField._properties['widget'](
            label='Email',
        ),
        searchable=True,
    ),
    TextField(
        name='bio',
        widget=RichWidget(
            label='Biography',
            rows=25
        ),
        storage = AnnotationStorage(migrate=True),
        default_output_type = 'text/x-html-safe',
        validators = ('isTidyHtmlWithCleanup',),
        searchable=True,
    ),
    LinesField(
        name='areasOfExpertise',
        widget=LinesWidget(
            label='Areas of Expertise',
            description="Enter one area of expertise per line."
        ),
        searchable=True,
    ),
    ImageField(
        name="image",
        required = False,
        storage = AnnotationStorage(migrate=True),
        languageIndependent = True,
        sizes= {'large'   : (768, 768),
                'preview' : (400, 400),
                'mini'    : (200, 200),
                'thumb'   : (128, 128),
                'tile'    :  (64, 64),
                'icon'    :  (32, 32),
                'listing' :  (16, 16),
            },
        validators = (('isNonEmptyFile', V_REQUIRED), ('checkNewsImageMaxSize', V_REQUIRED)),
        widget = ImageWidget(
            description = 'Image of yourself',
            label="Picture",
            show_content_type = False
        )
    )
),
)


ExpertSchema = BaseSchema.copy() + schema.copy()


class Expert(BaseContent, BrowserDefaultMixin, ATDocumentBase, ATCTImageTransform):
    """
    
    """
    
    security = ClassSecurityInfo()

    implements(interfaces.IExpert)

    meta_type = 'Expert'
    portal_type = "Expert"
    _at_rename_after_creation = True

    schema = ExpertSchema
    
    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return ATDocumentBase.__bobo_traverse__(self, REQUEST, name)
    
registerType(Expert, PRODUCT_NAME)