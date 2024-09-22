# Script to load zip templates

# Modules
import imp
from tkinter.messagebox import NO
import zipfile
from django.conf import settings
from django.template import TemplateDoesNotExist

# Functions

def load_template_source(template_name,template_dirs=None) -> tuple:
    template_zipfiles = getattr(settings,"TEMPLATE_ZIP_FILES",[])
    print(template_zipfiles)
    for name in template_zipfiles:
        try:
            z = zipfile.ZipFile(name)
            source = z.read(template_name)
            
        except (IOError,KeyError):
            continue
        z.close()
        template_path = "%s:%s" % (name,template_name)
        return (source,template_path)
    raise TemplateDoesNotExist(template_name)

load_template_source.is_usable = True