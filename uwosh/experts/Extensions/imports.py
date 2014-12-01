import xlrd, os, sys
from zope.app.component.hooks import getSite

path_to_excel = ""

for path in sys.path:
    if 'uwosh.experts' in path:
        path_to_excel = path

def getNumberOfContacts():
    
    book = xlrd.open_workbook("%s/uwosh/experts/Extensions/Contacts.xls" % path_to_excel)
    sheet = book.sheet_by_index(0)
    return sheet.nrows
    
def getRow(row_id):
    book = xlrd.open_workbook("%s/uwosh/experts/Extensions/Contacts.xls" % path_to_excel)
    sheet = book.sheet_by_index(0)
    return {
        'first_name': sheet.cell_value(rowx=row_id, colx=1),
        'last_name': sheet.cell_value(rowx=row_id, colx=2),
        'department': sheet.cell_value(rowx=row_id, colx=3),
        'title': sheet.cell_value(rowx=row_id, colx=4),
        'workPhone': sheet.cell_value(rowx=row_id, colx=5),
        'homePhone': sheet.cell_value(rowx=row_id, colx=6),
        'mobilePhone': sheet.cell_value(rowx=row_id, colx=7),
        'email': sheet.cell_value(rowx=row_id, colx=8),
        'bio': sheet.cell_value(rowx=row_id, colx=9),
        'areasOfExpertise': sheet.cell_value(rowx=row_id, colx=10)
    }

def dir(x):
    return dir(x)

def importContacts():
    
    site = getSite()
    
    expert_folder = None
    #get or create expert folder
    if 'experts' in site.objectIds():
        expert_folder = site['experts']
    else:
        site.invokeFactory(id="experts", type_name="Folder")
        expert_folder = site['experts']
        expert_folder.setTitle("Experts")
        
    book = xlrd.open_workbook("%s/uwosh/experts/Extensions/Contacts.xls" % path_to_excel)
    #only one worksheet
    sheet = book.sheet_by_index(0)      
    
    # Row Ids
    # 0 - id
    # 1 - First Name
    # 2 - Last Name
    # 3 - Department
    # 4 - Title
    # 5 - Work Phone
    # 6 - Home Phone
    # 7 - Mobile Phone
    # 8 - email
    # 9 - Bio
    # 10 - Areas of Expertise
    
    for row_id in range(1, sheet.nrows):
        fullname = sheet.cell_value(rowx=row_id, colx=1) + " " + sheet.cell_value(rowx=row_id, colx=2)
        id = fullname.replace(" ", "").replace(".", "")
        
        #create expert object
        expert_folder.invokeFactory(type_name="Expert", id=id)
        expert = expert_folder[id]
        
        #set the name
        expert.setTitle(fullname)
        
        #set department
        expert.setDepartment(sheet.cell_value(rowx=row_id, colx=3))
        
        #set professional Title
        expert.setProfessionalTitle(sheet.cell_value(rowx=row_id, colx=4))
        
        #set work phone
        expert.setWorkPhone(sheet.cell_value(rowx=row_id, colx=5))
        
        #set home phone
        expert.setHomePhone(sheet.cell_value(rowx=row_id, colx=6))
        
        #set mobile phone
        expert.setMobilePhone(sheet.cell_value(rowx=row_id, colx=7))
        
        #set email
        expert.setEmail(sheet.cell_value(rowx=row_id, colx=8))
        
        #set bio
        expert.setBio(sheet.cell_value(rowx=row_id, colx=9))
        
        # set Areas of Expertise
        # sometimes delimited by "," and other times by ";"
        areas = sheet.cell_value(rowx=row_id, colx=10)
        
        areas = areas.split(',')
        if len(areas) == 1:
            areas = areas[0].split(';')
        
        expert.setAreasOfExpertise(areas)
        expert.reindexObject()

