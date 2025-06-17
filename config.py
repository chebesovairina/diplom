from flask import Flask, render_template, request, redirect, url_for, send_file, json, session
from docx import Document
from docx.shared import Pt, RGBColor
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import re
import sqlite3
import requests
from API import prompt_api
import json
import random
from passlib.context import CryptContext

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
