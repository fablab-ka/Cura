#coding:utf8
"""
Helper module to get easy access to the path where resources are stored.
This is because the resource location is depended on the packaging method and OS
"""
__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import os
import sys
import glob
import platform
import locale

import gettext
import profile

if sys.platform.startswith('darwin'):
	try:
		#Foundation import can crash on some MacOS installs
		from Foundation import *
	except:
		pass

if sys.platform.startswith('darwin'):
	if hasattr(sys, 'frozen'):
		try:
			resourceBasePath = NSBundle.mainBundle().resourcePath()
		except:
			resourceBasePath = os.path.join(os.path.dirname(__file__), "../../../../../")
	else:
		resourceBasePath = os.path.join(os.path.dirname(__file__), "../../resources")
else:
	resourceBasePath = os.path.join(os.path.dirname(__file__), "../../resources")

def getPathForResource(dir, subdir, resource_name):
	assert os.path.isdir(dir), "{p} is not a directory".format(p=dir)
	path = os.path.normpath(os.path.join(dir, subdir, resource_name))
	if not os.path.isfile(path):
		return None
	return path

def getPathForImage(name):
	return getPathForResource(resourceBasePath, 'images', name)

def getPathForMesh(name):
	return getPathForResource(resourceBasePath, 'meshes', name)

def getPathForFirmware(name):
	return getPathForResource(resourceBasePath, 'firmware', name)

def getDefaultMachineProfiles():
	path = os.path.normpath(os.path.join(resourceBasePath, 'machine_profiles', '*.ini'))
	return glob.glob(path)

def getSimpleModeIniFiles(subdir, pattern = '*.ini'):
	machine_type = profile.getMachineSetting('machine_type')
	paths = []
	paths.append(os.path.normpath(os.path.expanduser(os.path.join('~', '.Cura', 'quickprint', machine_type, subdir))))
	paths.append(os.path.normpath(os.path.expanduser(os.path.join('~', '.Cura', 'quickprint', subdir))))
	paths.append(os.path.normpath(os.path.join(resourceBasePath, 'quickprint', machine_type, subdir)))
	paths.append(os.path.normpath(os.path.join(resourceBasePath, 'quickprint', subdir)))
	for path in paths:
		if os.path.isdir(path):
			files = sorted(glob.glob(os.path.join(path, pattern)))
			if len(files) > 0:
				return files
	return []


def getSimpleModeProfiles():
	return getSimpleModeIniFiles('profiles')

def getSimpleModeMaterials():
	return getSimpleModeIniFiles('materials')

def getSimpleModeOptions():
	return getSimpleModeIniFiles('options')

def setupLocalization(selectedLanguage = None):
	#Default to english
	languages = ['en']

	if selectedLanguage is not None:
		for item in getLanguageOptions():
			if item[1] == selectedLanguage and item[0] is not None:
				languages = [item[0]]
				break
	if languages[0] == 'AUTO':
		languages = ['en']
		defaultLocale = getDefaultLocale()
		if defaultLocale is not None:
			for item in getLanguageOptions():
				if item[0] == 'AUTO':
					continue
				if item[0] is not None and defaultLocale.startswith(item[0]):
					languages = [item[0]]

	locale_path = os.path.normpath(os.path.join(resourceBasePath, 'locale'))
	translation = gettext.translation('Cura', locale_path, languages, fallback=True)
	#translation.ugettext = lambda message: u'#' + message
	translation.install(unicode=True)

def getLanguageOptions():
	return [
		['AUTO', 'Autodetect'],
		['en', 'English'],
		['de', 'Deutsch'],
		['fr', 'French'],
		['tr', 'Turkish'],
		['ru', 'Russian'],
		# ['ko', 'Korean'],
		# ['zh', 'Chinese'],
		# ['nl', 'Nederlands'],
		# ['es', 'Spanish'],
		# ['po', 'Polish']
	]

def getDefaultLocale():
	defaultLocale = None

	# On Windows, we look for the actual UI language, as someone could have
	# an english windows but use a non-english locale.
	if platform.system() == "Windows":
		try:
			import ctypes

			windll = ctypes.windll.kernel32
			defaultLocale = locale.windows_locale[windll.GetUserDefaultUILanguage()]
		except:
			pass

	if defaultLocale is None:
		try:
			defaultLocale = locale.getdefaultlocale()[0]
		except:
			pass

	return defaultLocale
