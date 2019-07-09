from django.shortcuts import render

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from myapp.models import Document
from myapp.forms import DocumentForm

from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os

import re

from datetime import date

def list(request):
    # PDF Hochladen
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect auf aktuelle Seite
            return HttpResponseRedirect(reverse('list'))
    else:
        # Leeres Formular
        form = DocumentForm() 

    # Lade Bild zum Analysieren - neuester Upload
    documents = Document.objects.all()
    docToAnalyse = documents.last().docfile.path

    # OCR Funktionsaufruf
    resultText = ocr(docToAnalyse)

    # Potentielle Treffer für Handlungspartner
    allWords = resultText.split()
    name = [allWords[0], " ".join(allWords[0:2]), " ".join(allWords[0:3])]
 
    # Potentielle Treffer für das Transaktionsdatum
    transactionDates = re.findall('(\d+\.\d+\.\d+)',resultText) 

    currentDay = date.today()
    currentDay = currentDay.strftime("%m.%d.%Y")

    # Potentielle Treffer für Summe
    noWhitespace = resultText.replace(" ", "").replace(":", "").lower()
    sums1 = re.findall('(eur\d+.\d+)', noWhitespace)
    sums2 = re.findall('(summe\d+.\d+)', noWhitespace)
    sums3 = re.findall('(sum\d+.\d+)', noWhitespace)
    sums = sums1 + sums2 + sums3
    sums = [s.replace('eur', '').replace('summe', '').replace('sum', '') for s in sums]

    
    # Render list page with the documents and the form
    return render(request, 'list.html', {'documents': documents, 'form': form, 'doc': docToAnalyse, 'result': resultText, 'name': name, 'dates': transactionDates, 'today': currentDay, 'sums': sums})

def ocr(docToAnalyse):
    # PDF zu Bild
    pdfPages = convert_from_path(docToAnalyse, 300)
    pdfPages[0].save("myapp/media/temp_.jpg", 'JPEG')

    # OCR mit pytesseract, Ergebnisstring zurückgeben
    return str(((pytesseract.image_to_string(Image.open("myapp/media/temp_.jpg"))))) 


   