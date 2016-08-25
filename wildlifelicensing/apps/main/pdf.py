import os
from io import BytesIO
from datetime import date

from reportlab.lib import enums
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, ListFlowable, \
    KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, black, blue

from django.core.files import File
from django.conf import settings

from wildlifelicensing.apps.main.helpers import render_user_name

from ledger.accounts.models import Document

BW_DPAW_HEADER_LOGO = os.path.join(settings.BASE_DIR, 'wildlifelicensing', 'static', 'wl', 'img',
                                   'bw_dpaw_header_logo.png')

COLOUR_DPAW_HEADER_LOGO = os.path.join(settings.BASE_DIR, 'wildlifelicensing', 'static', 'wl', 'img',
                                       'colour_dpaw_header_logo.png')

DPAW_EMAIL = 'wildlifelicensing@dpaw.wa.gov.au'
DPAW_URL = 'dpaw.wa.gov.au'
DPAW_PHONE = '(08) 9219 9831'
DPAW_FAX = '(08) 9423 2242'
DPAW_PO_BOX = 'Locked Bag 104, Bentley Delivery Centre, Western Australia 6983'


PAGE_WIDTH, PAGE_HEIGHT = A4

DEFAULT_FONTNAME = 'Helvetica'
BOLD_FONTNAME = 'Helvetica-Bold'
BOLD_ITALIC_FONTNAME = 'Helvetica-BoldOblique'

VERY_LARGE_FONTSIZE = 14
LARGE_FONTSIZE = 12
MEDIUM_FONTSIZE = 10
SMALL_FONTSIZE = 8

PARAGRAPH_BOTTOM_MARGIN = 5

SECTION_BUFFER_HEIGHT = 10

DATE_FORMAT = '%d/%m/%Y'

HEADER_MARGIN = 10
HEADER_SMALL_BUFFER = 3

PAGE_MARGIN = 20
PAGE_TOP_MARGIN = 200

LETTER_HEADER_MARGIN = 30
LETTER_PAGE_MARGIN = 60
LETTER_IMAGE_WIDTH = 242
LETTER_IMAGE_HEIGHT = 55
LETTER_HEADER_RIGHT_LABEL_OFFSET = 400
LETTER_HEADER_RIGHT_INFO_OFFSET = 450
LETTER_HEADER_SMALL_BUFFER = 5
LETTER_ADDRESS_BUFFER_HEIGHT = 40
LETTER_BLUE_FONT = 0x045690

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='InfoTitleLargeCenter', fontName=BOLD_FONTNAME, fontSize=LARGE_FONTSIZE,
                          spaceAfter=PARAGRAPH_BOTTOM_MARGIN, alignment=enums.TA_CENTER))
styles.add(ParagraphStyle(name='InfoTitleVeryLargeCenter', fontName=BOLD_FONTNAME, fontSize=VERY_LARGE_FONTSIZE,
                          spaceAfter=PARAGRAPH_BOTTOM_MARGIN * 2, alignment=enums.TA_CENTER))
styles.add(ParagraphStyle(name='InfoTitleLargeLeft', fontName=BOLD_FONTNAME, fontSize=LARGE_FONTSIZE,
                          spaceAfter=PARAGRAPH_BOTTOM_MARGIN, alignment=enums.TA_LEFT,
                          leftIndent=PAGE_WIDTH / 10, rightIndent=PAGE_WIDTH / 10))
styles.add(ParagraphStyle(name='InfoTitleLargeRight', fontName=BOLD_FONTNAME, fontSize=LARGE_FONTSIZE,
                          spaceAfter=PARAGRAPH_BOTTOM_MARGIN, alignment=enums.TA_RIGHT,
                          rightIndent=PAGE_WIDTH / 10))
styles.add(ParagraphStyle(name='BoldLeft', fontName=BOLD_FONTNAME, fontSize=MEDIUM_FONTSIZE, alignment=enums.TA_LEFT))
styles.add(ParagraphStyle(name='BoldRight', fontName=BOLD_FONTNAME, fontSize=MEDIUM_FONTSIZE, alignment=enums.TA_RIGHT))
styles.add(ParagraphStyle(name='Center', alignment=enums.TA_CENTER))
styles.add(ParagraphStyle(name='Left', alignment=enums.TA_LEFT))
styles.add(ParagraphStyle(name='Right', alignment=enums.TA_RIGHT))
styles.add(ParagraphStyle(name='LetterLeft', fontSize=LARGE_FONTSIZE, alignment=enums.TA_LEFT))
styles.add(ParagraphStyle(name='LetterBoldLeft', fontName=BOLD_FONTNAME, fontSize=LARGE_FONTSIZE, alignment=enums.TA_LEFT))


def _create_licence_header(canvas, doc, draw_page_number=True):
    canvas.setFont(BOLD_FONTNAME, LARGE_FONTSIZE)

    current_y = PAGE_HEIGHT - HEADER_MARGIN

    canvas.drawCentredString(PAGE_WIDTH / 2, current_y - LARGE_FONTSIZE, 'DEPARTMENT OF PARKS AND WILDLIFE')

    current_y -= 30

    dpaw_header_logo = ImageReader(BW_DPAW_HEADER_LOGO)
    dpaw_header_logo_size = dpaw_header_logo.getSize()
    canvas.drawImage(dpaw_header_logo, HEADER_MARGIN, current_y - dpaw_header_logo_size[1])

    current_x = HEADER_MARGIN + dpaw_header_logo_size[0] + 5

    canvas.setFont(DEFAULT_FONTNAME, SMALL_FONTSIZE)

    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + HEADER_SMALL_BUFFER), 'Enquiries:')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + HEADER_SMALL_BUFFER) * 2, 'Telephone:')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + HEADER_SMALL_BUFFER) * 3, 'Facsimile:')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + HEADER_SMALL_BUFFER) * 4, 'Web Site:')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + HEADER_SMALL_BUFFER) * 5, 'Correspondance:')

    current_x += 80

    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + HEADER_SMALL_BUFFER),
                      '17 DICK PERRY AVE, KENSINGTON, WESTERN AUSTRALIA')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + HEADER_SMALL_BUFFER) * 2, '08 9219 9000')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + HEADER_SMALL_BUFFER) * 3, '08 9219 8242')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + HEADER_SMALL_BUFFER) * 4, doc.site_url)

    canvas.setFont(BOLD_FONTNAME, SMALL_FONTSIZE)
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + HEADER_SMALL_BUFFER) * 5, 'Locked Bag 30')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + HEADER_SMALL_BUFFER) * 6,
                      'Bentley Delivery Centre WA 6983')

    canvas.setFont(BOLD_FONTNAME, LARGE_FONTSIZE)

    current_y -= 36
    current_x += 200

    if draw_page_number:
        canvas.drawString(current_x, current_y - (LARGE_FONTSIZE + HEADER_SMALL_BUFFER), 'PAGE')

    if hasattr(doc, 'licence') and doc.licence.licence_number is not None and doc.licence.licence_sequence:
        canvas.drawString(current_x, current_y - (LARGE_FONTSIZE + HEADER_SMALL_BUFFER) * 2, 'NO.')

    canvas.setFont(DEFAULT_FONTNAME, LARGE_FONTSIZE)

    current_x += 50

    if draw_page_number:
        canvas.drawString(current_x, current_y - (LARGE_FONTSIZE + HEADER_SMALL_BUFFER), str(canvas.getPageNumber()))

    if hasattr(doc, 'licence') and doc.licence.licence_number is not None and doc.licence.licence_sequence:
        canvas.drawString(current_x, current_y - (LARGE_FONTSIZE + HEADER_SMALL_BUFFER) * 2,
                          '%s-%d' % (doc.licence.licence_number, doc.licence.licence_sequence))


def _get_authorised_person_names(application):
    def __find_authorised_persons_dict(data):
        authorised_persons = []
        for item in data:
            if isinstance(item, list):
                authorised_persons = __find_authorised_persons_dict(item)
                if len(authorised_persons) > 0:
                    return authorised_persons
            if isinstance(item, dict):
                if 'authorised_persons' in item:
                    return item['authorised_persons']
                else:
                    for value in item.values():
                        if isinstance(value, list):
                            authorised_persons = __find_authorised_persons_dict(value)
                            if len(authorised_persons) > 0:
                                return authorised_persons

        return authorised_persons

    authorised_person_names = []

    for ap in __find_authorised_persons_dict(application.data):
        if ap.get('ap_given_names') and ap.get('ap_surname'):
            authorised_person_names.append('%s %s' % (ap['ap_given_names'], ap['ap_surname']))

    return authorised_person_names


def _get_species(application):
    def __find_species_dict(data):
        species = []
        for item in data:
            if isinstance(item, list):
                species = __find_species_dict(item)
                if len(species) > 0:
                    return species
            if isinstance(item, dict):
                if 'species_summary' in item:
                    return item['species_summary']
                else:
                    for value in item.values():
                        if isinstance(value, list):
                            species = __find_species_dict(value)
                            if len(species) > 0:
                                return species

        return species

    species_names_and_count = []

    for s in __find_species_dict(application.data):
        if s.get('species_name') and s.get('species_count'):
            species_names_and_count.append((s['species_name'], s['species_count']))

    return species_names_and_count


def _create_licence(licence_buffer, licence, application, site_url, original_issue_date):
    every_page_frame = Frame(PAGE_MARGIN, PAGE_MARGIN, PAGE_WIDTH - 2 * PAGE_MARGIN,
                             PAGE_HEIGHT - 160, id='EveryPagesFrame')
    every_page_template = PageTemplate(id='EveryPages', frames=every_page_frame, onPage=_create_licence_header)

    doc = BaseDocTemplate(licence_buffer, pageTemplates=[every_page_template], pagesize=A4)

    # this is the only way to get data into the onPage callback function
    doc.licence = licence
    doc.site_url = site_url

    licence_table_style = TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')])

    elements = []

    elements.append(Paragraph(licence.licence_type.act, styles['InfoTitleLargeCenter']))
    elements.append(Paragraph(licence.licence_type.code.upper(), styles['InfoTitleLargeCenter']))
    elements.append(Paragraph(licence.licence_type.name, styles['InfoTitleVeryLargeCenter']))
    elements.append(Paragraph(licence.licence_type.statement, styles['InfoTitleLargeLeft']))
    elements.append(Paragraph(licence.licence_type.authority, styles['InfoTitleLargeRight']))

    # licence conditions
    if application.conditions.exists():
        elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))
        elements.append(Paragraph('Conditions', styles['InfoTitleLargeCenter']))
        conditionList = ListFlowable(
            [Paragraph(condition.text, styles['Left']) for condition in application.conditions.all()],
            bulletFontName=BOLD_FONTNAME, bulletFontSize=MEDIUM_FONTSIZE)
        elements.append(conditionList)

    # purpose
    if licence.purpose:
        elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))

        purposes = []
        for purpose in licence.purpose.split('\r\n'):
            if purpose:
                purposes.append(Paragraph(purpose, styles['Left']))
            else:
                purposes.append(Spacer(1, SECTION_BUFFER_HEIGHT))

        elements.append(Table([[Paragraph('Purpose', styles['BoldLeft']), purposes]],
                              colWidths=(100, PAGE_WIDTH - (2 * PAGE_MARGIN) - 100),
                              style=licence_table_style))

    # locations
    if licence.locations:
        elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))

        locations = []
        for location in licence.locations.split('\r\n'):
            if location:
                locations.append(Paragraph(location, styles['Left']))

        elements.append(Table([[Paragraph('Locations', styles['BoldLeft']), locations]],
                              colWidths=(100, PAGE_WIDTH - (2 * PAGE_MARGIN) - 100),
                              style=licence_table_style))

    # authorised persons
    authorised_persons = _get_authorised_person_names(application)
    if len(authorised_persons) > 0:
        elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))
        authorised_persons_paragraph = [Paragraph(ap, styles['Left']) for ap in authorised_persons]
        elements.append(Table([[Paragraph('Authorised Persons', styles['BoldLeft']), authorised_persons_paragraph]],
                              colWidths=(100, PAGE_WIDTH - (2 * PAGE_MARGIN) - 100),
                              style=licence_table_style))

    # species
    species = _get_species(application)
    if len(species) > 0:
        elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))
        species_names = [Paragraph(s[0], styles['Left']) for s in species]
        species_count = [Paragraph(s[1], styles['Left']) for s in species]
        section_width = (PAGE_WIDTH - (2 * PAGE_MARGIN) - 100) / 2

        elements.append(Table([[Paragraph('Species', styles['BoldLeft']), Paragraph('Name', styles['BoldLeft']),
                                Paragraph('Count', styles['BoldLeft'])],
                               ['', species_names, species_count]],
                              colWidths=(100, section_width, section_width), style=licence_table_style))

    # additional information
    if licence.additional_information:
        elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))

        additional_information_paragraphs = []
        for paragraph in licence.additional_information.split('\r\n'):
            if paragraph:
                additional_information_paragraphs.append(Paragraph(paragraph, styles['Left']))

        elements.append(Table([[Paragraph('Additional Information', styles['BoldLeft']),
                                additional_information_paragraphs]],
                              colWidths=(100, PAGE_WIDTH - (2 * PAGE_MARGIN) - 100),
                              style=licence_table_style))

    # delegation holds the dates, licencee and issuer details.
    delegation = []

    # dates and licensing officer
    dates_licensing_officer_table_style = TableStyle([('VALIGN', (0, 0), (-2, -1), 'TOP'),
                                                      ('VALIGN', (0, 0), (-1, -1), 'BOTTOM')])

    delegation.append(Spacer(1, SECTION_BUFFER_HEIGHT))
    date_headings = [Paragraph('Date of Issue', styles['BoldLeft']), Paragraph('Valid From', styles['BoldLeft']),
                     Paragraph('Date of Expiry', styles['BoldLeft'])]
    date_values = [Paragraph(licence.issue_date.strftime(DATE_FORMAT), styles['Left']),
                   Paragraph(licence.start_date.strftime(DATE_FORMAT), styles['Left']),
                   Paragraph(licence.end_date.strftime(DATE_FORMAT), styles['Left'])]

    if original_issue_date is not None:
        date_headings.insert(0, Paragraph('Original Date of Issue', styles['BoldLeft']))
        date_values.insert(0, Paragraph(original_issue_date.strftime(DATE_FORMAT), styles['Left']))

    delegation.append(Table([[date_headings, date_values]],
                            colWidths=(120, PAGE_WIDTH - (2 * PAGE_MARGIN) - 120),
                            style=dates_licensing_officer_table_style))

    # licensee details
    delegation.append(Spacer(1, SECTION_BUFFER_HEIGHT))
    address = application.applicant_profile.postal_address
    address_paragraphs = [Paragraph(address.line1, styles['Left']), Paragraph(address.line2, styles['Left']),
                          Paragraph(address.line3, styles['Left']),
                          Paragraph('%s %s %s' % (address.locality, address.state, address.postcode), styles['Left']),
                          Paragraph(address.country.name, styles['Left'])]
    delegation.append(Table([[[Paragraph('Licensee:', styles['BoldLeft']), Paragraph('Address', styles['BoldLeft'])],
                              [Paragraph(render_user_name(application.applicant),
                                         styles['Left'])] + address_paragraphs]],
                            colWidths=(120, PAGE_WIDTH - (2 * PAGE_MARGIN) - 120),
                            style=licence_table_style))

    delegation.append(Spacer(1, SECTION_BUFFER_HEIGHT))
    delegation.append(Paragraph('Issued by a Wildlife Licensing Officer of the Department of Parks and Wildlife '
                                'under delegation from the Minister for Environment pursuant to section 133(1) '
                                'of the Conservation and Land Management Act 1984.', styles['Left']))

    elements.append(KeepTogether(delegation))

    doc.build(elements)

    return licence_buffer


def _create_letter_header_footer(canvas, doc):
    canvas.setFont(BOLD_FONTNAME, LARGE_FONTSIZE)

    current_y = PAGE_HEIGHT - LETTER_HEADER_MARGIN

    dpaw_header_logo = ImageReader(COLOUR_DPAW_HEADER_LOGO)
    canvas.drawImage(dpaw_header_logo, LETTER_HEADER_MARGIN, current_y - LETTER_IMAGE_HEIGHT,
                     width=LETTER_IMAGE_WIDTH, height=LETTER_IMAGE_HEIGHT)

    canvas.setFillColor(HexColor(LETTER_BLUE_FONT))

    canvas.setFont(DEFAULT_FONTNAME, SMALL_FONTSIZE)

    current_x = LETTER_HEADER_RIGHT_LABEL_OFFSET

    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + LETTER_HEADER_SMALL_BUFFER), 'Your ref:')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + LETTER_HEADER_SMALL_BUFFER) * 2, 'Our ref:')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + LETTER_HEADER_SMALL_BUFFER) * 3, 'Enquiries:')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + LETTER_HEADER_SMALL_BUFFER) * 4, 'Phone:')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + LETTER_HEADER_SMALL_BUFFER) * 5, 'Email:')

    current_x = LETTER_HEADER_RIGHT_INFO_OFFSET

    canvas.setFillColor(black)

    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + LETTER_HEADER_SMALL_BUFFER), '')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + LETTER_HEADER_SMALL_BUFFER) * 2, '')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + LETTER_HEADER_SMALL_BUFFER) * 3, '')
    canvas.drawString(current_x, current_y - (SMALL_FONTSIZE + LETTER_HEADER_SMALL_BUFFER) * 4, '(08) 9219 9831')

    # draw email address as hyperlink
    email_address = DPAW_EMAIL

    current_y = current_y - (SMALL_FONTSIZE + LETTER_HEADER_SMALL_BUFFER) * 5
    canvas.setFillColor(blue)
    canvas.drawString(current_x, current_y, email_address)

    email_address_width = canvas.stringWidth(email_address)

    linkRect = (current_x, current_y, current_x + email_address_width, current_y)
    canvas.linkURL('mailto:{}'.format(email_address), linkRect)

    current_x = PAGE_WIDTH - LETTER_HEADER_MARGIN
    current_y = LETTER_HEADER_MARGIN

    canvas.setFont(DEFAULT_FONTNAME, SMALL_FONTSIZE)
    canvas.setFillColor(HexColor(LETTER_BLUE_FONT))

    canvas.drawRightString(current_x, current_y, DPAW_URL)
    canvas.drawRightString(current_x, current_y + SMALL_FONTSIZE,
                           'Phone: {} Fax: {} Email: {}'.format(DPAW_PHONE, DPAW_FAX, DPAW_EMAIL))
    canvas.drawRightString(current_x, current_y + SMALL_FONTSIZE * 2, DPAW_PO_BOX)

    canvas.setFont(BOLD_ITALIC_FONTNAME, SMALL_FONTSIZE)

    canvas.drawRightString(current_x, current_y + SMALL_FONTSIZE * 3, 'Wildlife Licensing Section')


def _create_letter_address(licence):
    addressee = licence.holder
    address = licence.profile.postal_address

    address_elements = []

    address_elements.append(Spacer(1, LETTER_ADDRESS_BUFFER_HEIGHT))

    address_elements.append(Paragraph(addressee.get_full_name(), styles['LetterLeft']))

    if licence.profile.institution:
        address_elements.append(Paragraph(licence.profile.institution, styles['LetterLeft']))

    address_elements.append(Paragraph(address.line1, styles['LetterLeft']))

    if address.line2:
        address_elements.append(Paragraph(address.line2, styles['LetterLeft']))

    if address.line3:
        address_elements.append(Paragraph(address.line3, styles['LetterLeft']))

    address_elements.append(Paragraph('{} {} {}'.format(address.locality, address.state, address.postcode),
                                      styles['LetterLeft']))

    return address_elements


def _create_letter_signature():
    signature_elements = []
    signature_elements.append(Paragraph('Yours sincerely', styles['LetterLeft']))
    signature_elements.append(Spacer(1, SECTION_BUFFER_HEIGHT * 4))
    signature_elements.append(Paragraph('from Jim Sharp', styles['LetterLeft']))
    signature_elements.append(Paragraph('DIRECTOR GENERAL', styles['LetterLeft']))
    signature_elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))

    signature_elements.append(Paragraph(date.today().strftime(DATE_FORMAT), styles['LetterLeft']),)

    return signature_elements


def _create_cover_letter(cover_letter_buffer, licence, site_url):
    cover_letter_frame = Frame(LETTER_PAGE_MARGIN, LETTER_PAGE_MARGIN, PAGE_WIDTH - 2 * LETTER_PAGE_MARGIN,
                               PAGE_HEIGHT - 160, id='CoverLetterFrame')

    every_cover_letter_template = PageTemplate(id='CoverLetter', frames=cover_letter_frame, onPage=_create_letter_header_footer)

    doc = BaseDocTemplate(cover_letter_buffer, pageTemplates=[every_cover_letter_template], pagesize=A4)

    elements = []

    elements += _create_letter_address(licence)

    elements.append(Spacer(1, LETTER_ADDRESS_BUFFER_HEIGHT))

    elements.append(Paragraph('Dear {}'.format(licence.holder.get_full_name()), styles['LetterLeft']))
    elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))
    elements.append(Paragraph('{}'.format(licence.licence_type.name), styles['LetterBoldLeft'])),
    elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))
    elements.append(Paragraph('Please find attached licence', styles['LetterLeft']))
    elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))
    elements.append(Paragraph('Please ensure that all the licence conditions are complied with, including the '
                              'forwarding of a return at the end of the licence period.', styles['LetterLeft']))
    elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))

    if licence.cover_letter_message:
        for message in licence.cover_letter_message.split('\r\n'):
            if message:
                elements.append(Paragraph(message, styles['LetterLeft']))
            else:
                elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))

        elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))

    elements.append(Paragraph('If you have any queries, please contact Mr Danny Stefoni on 9219 9833.', styles['LetterLeft']))
    elements.append(Spacer(1, SECTION_BUFFER_HEIGHT))

    elements += _create_letter_signature()

    doc.build(elements)

    return cover_letter_buffer


def _create_licence_renewal_elements(licence):
    return [
        Paragraph('Dear {}'.format(licence.holder.get_full_name()), styles['LetterLeft']),
        Spacer(1, SECTION_BUFFER_HEIGHT),
        Paragraph('This is a reminder that your licence:', styles['LetterLeft']),
        Spacer(1, SECTION_BUFFER_HEIGHT),
        Paragraph('{}'.format(licence.licence_type.name), styles['LetterBoldLeft']),
        Spacer(1, SECTION_BUFFER_HEIGHT),
        Paragraph('is due to expire on {}.'.format(licence.end_date.strftime(DATE_FORMAT)), styles['LetterLeft']),
        Spacer(1, SECTION_BUFFER_HEIGHT),
        Paragraph('Please note that you are required to submit an electronic return and that '
                  'the licence cannot be renewed until this.', styles['LetterLeft']),
        Spacer(1, SECTION_BUFFER_HEIGHT),
        Paragraph('If you have any queries, please contact Mr Danny Stefoni on 9219 9833 or '
                  'email to wildlifelicensing@dpaw.wa.gov.au.', styles['LetterLeft']),
        Spacer(1, SECTION_BUFFER_HEIGHT),
    ]


def _create_licence_renewal(licence_renewal_buffer, licence, site_url):
    licence_renewal_frame = Frame(LETTER_PAGE_MARGIN, LETTER_PAGE_MARGIN, PAGE_WIDTH - 2 * LETTER_PAGE_MARGIN,
                                  PAGE_HEIGHT - 160, id='LicenceRenewalFrame')
    licence_renewal_template = PageTemplate(id='LicenceRenewalFrame', frames=licence_renewal_frame, onPage=_create_letter_header_footer)

    doc = BaseDocTemplate(licence_renewal_buffer, pageTemplates=[licence_renewal_template], pagesize=A4)

    elements = _create_letter_address(licence) + [Spacer(1, LETTER_ADDRESS_BUFFER_HEIGHT)] + \
        _create_licence_renewal_elements(licence) + _create_letter_signature()

    doc.build(elements)

    return licence_renewal_buffer


def _create_bulk_licence_renewal(licences, site_url, buf=None):
    bulk_licence_renewal_frame = Frame(LETTER_PAGE_MARGIN, LETTER_PAGE_MARGIN, PAGE_WIDTH - 2 * LETTER_PAGE_MARGIN,
                                       PAGE_HEIGHT - 160, id='BulkLicenceRenewalFrame')
    bulk_licence_renewal_template = PageTemplate(id='BulkLicenceRenewalFrame', frames=bulk_licence_renewal_frame,
                                                 onPage=_create_letter_header_footer)

    if buf is None:
        buf = BytesIO()
    doc = BaseDocTemplate(buf, pageTemplates=[bulk_licence_renewal_template], pagesize=A4)

    # this is the only way to get data into the onPage callback function
    doc.site_url = site_url
    all_elements = []
    for licence in licences:
        all_elements += _create_letter_address(licence) + [Spacer(1, LETTER_ADDRESS_BUFFER_HEIGHT)] + \
            _create_licence_renewal_elements(licence) + _create_letter_signature()
        all_elements.append(PageBreak())
    doc.build(all_elements)
    return doc


def create_licence_pdf_document(filename, licence, application, site_url, original_issue_date):
    licence_buffer = BytesIO()

    _create_licence(licence_buffer, licence, application, site_url, original_issue_date)

    document = Document.objects.create(name=filename)
    document.file.save(filename, File(licence_buffer), save=True)

    licence_buffer.close()

    return document


def create_licence_pdf_bytes(filename, licence, application, site_url, original_issue_date):
    licence_buffer = BytesIO()

    _create_licence(licence_buffer, licence, application, site_url, original_issue_date)

    # Get the value of the BytesIO buffer
    value = licence_buffer.getvalue()
    licence_buffer.close()

    return value


def create_cover_letter_pdf_document(filename, licence, site_url):
    cover_letter_buffer = BytesIO()

    _create_cover_letter(cover_letter_buffer, licence, site_url)

    document = Document.objects.create(name=filename)
    document.file.save(filename, File(cover_letter_buffer), save=True)

    cover_letter_buffer.close()

    return document


def create_licence_renewal_pdf_bytes(filename, licence, site_url):
    licence_renewal_buffer = BytesIO()

    _create_licence_renewal(licence_renewal_buffer, licence, site_url)

    value = licence_renewal_buffer.getvalue()
    licence_renewal_buffer.close()

    return value


def bulk_licence_renewal_pdf_bytes(licences, site_url):
    doc = None
    try:
        doc = _create_bulk_licence_renewal(licences, site_url)
        return doc.filename.getvalue()
    finally:
        if doc:
            doc.filename.close()