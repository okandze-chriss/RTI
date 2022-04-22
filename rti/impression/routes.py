import os
import uuid
from datetime import date, timedelta
from io import StringIO

from flask import render_template, url_for, current_app, request, Response, make_response
from flask_login import login_required, current_user
import pdfkit

from rti.impression import impression


'''
@impression.route('/dashboard/print/calendar')
@login_required
def print_calendar():
    Download_FOLDER = "C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe"
    url = request.base_url + '/presence'
    try:
        filename = str(uuid.uuid4()) + '.pdf'
        config = pdfkit.configuration(wkhtmltopdf=Download_FOLDER)
        options = {
            'page-size': 'Legal',
            'orientation': 'Landscape'
        }
        pdfkit.from_url(url, filename, configuration=config, options=options)
        pdfDownload = open(filename, 'rb').read()
        os.remove(filename)
        return Response(
            pdfDownload,
            mimetype="application/pdf",
            headers={
                "Content-disposition": "attachment; filename=" + filename,
                "Content-type": "application/force-download"
            }
        )
    except ValueError:
        print("Oops! ")


@impression.route('/dashboard/print/calendar/presence')
def print_calendar_route():
    # months
    annee = date.today().year
    mois = [['03', 'MARS'], ['04', 'AVRIL'], ['05', 'MAI'], ['06', 'JUIN'], ['07', 'JUILLET'], ['08', 'AOÛT'],
            ['09', 'SEPTEMBRE'],
            ['10', 'OCTOBRE'], ['11', 'NOVEMBRE']]
    journees = load_all_journees()
    return render_template('impression/calendrier.html', annee=annee, mois=mois, journees=journees)


@impression.route('/dashboard/print/calendar/travaux')
@login_required
def print_calendar_travaux():
    Download_FOLDER = "C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe"
    url = request.base_url + '/pdf'
    try:
        filename = str(uuid.uuid4()) + '.pdf'
        config = pdfkit.configuration(wkhtmltopdf=Download_FOLDER)
        options = {
            'page-size': 'Legal',
            'orientation': 'Landscape'
        }
        pdfkit.from_url(url, filename, configuration=config, options=options)
        pdfDownload = open(filename, 'rb').read()
        os.remove(filename)
        return Response(
            pdfDownload,
            mimetype="application/pdf",
            headers={
                "Content-disposition": "attachment; filename=" + filename,
                "Content-type": "application/force-download"
            }
        )
    except ValueError:
        print("Oops! ")


@impression.route('/dashboard/print/calendar/travaux/pdf')
def print_calendar_travaux_route():
    # months
    annee = date.today().year
    mois = [['03', 'MARS'], ['04', 'AVRIL'], ['05', 'MAI'], ['06', 'JUIN'], ['07', 'JUILLET'], ['08', 'AOÛT'],
            ['09', 'SEPTEMBRE'],
            ['10', 'OCTOBRE'], ['11', 'NOVEMBRE']]
    journees = load_all_journees()
    return render_template('impression/travaux.html', annee=annee, mois=mois, journees=journees)'''
