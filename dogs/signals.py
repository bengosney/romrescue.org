from django.db.models.signals import post_save
from django.dispatch import receiver

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from .models import Dog

def get_sheets_auth():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('google-creds.json', scope)

    return gspread.authorize(credentials)

def get_sheet(sheet_name):
    gc = get_sheets_auth()

    try:
        print("Opening sheet")
        dog_list = gc.open(sheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        print("Sheet not found, creating")
        dog_list = gc.create(sheet_name)

    return dog_list

@receiver(post_save, sender=Dog)
def update_google_sheet(sender, instance, **kwargs):
    dog_object = instance
    dog_list = get_sheet("Dog List")
    
    dog_list.share('ben@romrescue.org', perm_type='user', role='writer', notify=False)

    sheets = []
    for status in Dog.STATUS:
        sheets.append(status[0])
        
    to_add = sheets
    for worksheet in dog_list.worksheets():
        if worksheet.title in to_add:
            to_add.remove(worksheet.title)
        
    for sheet_name in to_add:
        dog_list.add_worksheet(sheet_name, 10, 30)


    worksheets = {}
    titles = [
        'Website ID',
        'Name',
        'DOB',
        'Gender',
        'Size',
        'Location',
        'Reserved',
        'URL',
    ]

    for worksheet in dog_list.worksheets():
        title_range = "A1:%s" % gspread.utils.rowcol_to_a1(1,len(titles))
        title_cells = worksheet.range(title_range)
    
        for title_cell in title_cells:
            title_cell.value = titles[title_cell.col - 1]

        worksheet.update_cells(title_cells)
        worksheets[worksheet.title] = worksheet



    data = [
        dog_object.sheet_id,
        dog_object.name,
        dog_object.dob,
        dog_object.gender,
        dog_object.size,
        dog_object.location,
        dog_object.reserved,
        "http://www.romrescue.org%s" % dog_object.correct_url,
    ]
    
    for worksheet in dog_list.worksheets():
        if worksheet != worksheets[dog_object.dogStatus]:
            try:
                found = worksheet.find(dog_object.sheet_id)
                tmp = worksheet.row_values(found.row)
                tmp[0:len(data)] = data
                data = tmp
                worksheet.delete_row(found.row)
            except gspread.exceptions.CellNotFound:
                pass
            

    worksheet = worksheets[dog_object.dogStatus]
    update_row = 0
    try:
        print("looking for %s" % dog_object.sheet_id)
        found = worksheet.find(dog_object.sheet_id)
        gspread.utils.rowcol_to_a1(1,len(titles))
        update_row = found.row
    except gspread.exceptions.CellNotFound:
        print("not found, looking for empty row")
        str_list = filter(None, worksheet.col_values(1))
        if len(str_list) != len(worksheet.col_values(1)):
            update_row = len(str_list) + 1
        

    if update_row > 0:
        print("Updating row")
        update_range ="%s:%s" % (
            gspread.utils.rowcol_to_a1(update_row, 1),
            gspread.utils.rowcol_to_a1(update_row, len(data))
        )
        cells = worksheet.range(update_range)
        for cell in cells:
            cell.value = data[cell.col - 1]
            worksheet.update_cells(cells)
    else:
        print("couldn't find empty row, appending")
        worksheet.append_row(data)
        worksheet.resize(worksheet.row_count + 10)
        

