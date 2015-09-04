import glob
import os
import json

from flask import render_template, jsonify, request, url_for, make_response, Response

from app import app


#
# fake DAO for svg repository
#

svgDirAbsolute = os.path.join(app.static_folder, 'svg-repo')
svgFilesAbsolute = glob.glob(os.path.join(svgDirAbsolute, '*.svg'))
svgFileNames = list(map(lambda f: os.path.split(f)[1], svgFilesAbsolute))


#
# pages/templates
#

@app.route('/')
def index():
    return render_template("index.html", svgFileNames=svgFileNames)


@app.route('/docs/<fileName>')
def editDocument(fileName):
    return render_template("edit.html", fileName=fileName)


#
# REST endpoints
#

@app.route('/docs/<fileName>/annotations')
def getAnnotationsJsonForFileName(fileName):
    """
    :param fileName: the svg file
    :return: a response containing the annotation json for an SVG file
    """
    svgFileNameAbs = os.path.join(svgDirAbsolute, fileName)
    svgFileRoot = os.path.splitext(svgFileNameAbs)[0]
    annotationsJsonFileName = svgFileRoot + '.json'
    with open(annotationsJsonFileName) as annotsJsonFile:
        annotationsList = annotsJsonFile.read()
        response = make_response(annotationsList, 202)  # TypeError: 'list' object is not callable
        response.mimetype = 'application/json'
        return response


@app.route('/docs/<fileName>/text')
def getTextForDocumentRectangle(fileName):
    """
    A placeholder for the domain-specific application that finds the text in an SVG file that's bounded by a rectangle.

    :param fileName: the svg file
    :return: a string for the rectangle in the svg file specified by query parameters: x, y, width, and height
    """
    x = request.args.get('x')
    y = request.args.get('y')
    width = request.args.get('width')
    height = request.args.get('height')
    return 'Text @ <{},{} - {}x{}>'.format(x, y, width, height)
