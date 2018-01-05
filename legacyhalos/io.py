"""
legacyhalos.io
==============

Code to read and write the various legacyhalos files.

"""
from __future__ import absolute_import, division, print_function

import os
import numpy as np
from glob import glob

def get_objid(cat):
    """Build a unique object ID based on the redmapper mem_match_id.

    Args:
      cat - must be a redmapper catalog or a catalog that has MEM_MATCH_ID.

    """
    lsdir = legacyhalos_dir()

    objid, objdir = list(), list()
    for ii, memid in enumerate(np.atleast_1d(cat.mem_match_id)):
        objid.append('{:07d}'.format(memid))
        objdir.append(os.path.join(lsdir, 'analysis', objid[ii]))
    
    return np.array(objid), np.array(objdir)

def legacyhalos_dir():
    if 'LEGACYHALOS_DIR' not in os.environ:
        print('Required ${LEGACYHALOS_DIR environment variable not set.')
        raise EnvironmentError
    return os.path.abspath(os.getenv('LEGACYHALOS_DIR'))

def analysis_dir():
    adir = os.path.join(legacyhalos_dir(), 'analysis')
    if not os.path.isdir(adir):
        os.makedirs(adir, exist_ok=True)
    return adir

def read_catalog(extname='LSPHOT', upenn=True, isedfit=False, columns=None):
    """Read the various catalogs.

    Args:
      upenn - Restrict to the UPenn-matched catalogs.

    """
    from astrometry.util.fits import fits_table

    suffix = ''
    if isedfit:
        suffix = '-isedfit'
    elif upenn:
        suffix = '-upenn'
    else:
        print('Unrecognized suffix!')
        raise ValueError

    lsdir = legacyhalos_dir()
    catfile = os.path.join(lsdir, 'legacyhalos-parent{}.fits'.format(suffix))
    
    cat = fits_table(catfile, ext=extname, columns=columns)

    return cat
