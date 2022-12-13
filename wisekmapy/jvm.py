#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import pdb
try:
    import jpype
except ImportError:
    pass


def init_jvm(jvmpath=None, wkb_jar_path=None):
    """
    Initializes the Java virtual machine (JVM).
    :param jvmpath: The path of the JVM. If left empty, inferred by :py:func:`jpype.getDefaultJVMPath`.
    :param wkb_jar_path: The path of the WISE KMA Black jar file.
    """

    if jpype.isJVMStarted():
        logging.warning('JVM is already running. Do not init twice!')
        return

    if wkb_jar_path is None:
        logging.error('Check WISE KMA Black jar file')
        return

    folder_suffix = [
        '{0}',
        '{0}{1}'+wkb_jar_path,
    ]

    javadir = '%s%s' % (os.path.dirname(os.path.realpath(__file__)), os.sep)

    args = [javadir, os.sep]
    classpath = os.pathsep.join(f.format(*args) for f in folder_suffix)
    libpath = '%s%slib' % (os.path.dirname(os.path.realpath(__file__)), os.sep)

    jvmpath = jvmpath or jpype.getDefaultJVMPath()

    # NOTE: Temporary patch for Issue #76. Erase when possible.
    # Defensive code for 'darwin' platform
    if sys.platform == 'darwin'\
            and jvmpath.find('1.7.0') > 0\
            and jvmpath.endswith('libjvm.dylib'):
        jvmpath = '%s/lib/jli/libjli.dylib' % jvmpath.split('/lib/')[0]

    # Start JVM
    # -ea : enable assertion
    # -Xmx2048m : maximum memory size (2048 mb)
    # print(libpath)
    # print(classpath)
    if jvmpath:
        jpype.startJVM(jvmpath, '-Djava.library.path=%s' % libpath,
                                '-Djava.class.path=%s' % classpath,
                                '-Dfile.encoding=UTF8',
                                '-ea', '-Xmx4g', convertStrings=True)
        print('JVM started')
    else:
        raise ValueError("Please specify the JVM path.")


if __name__ == "__main__" :
    if len(sys.argv) != 2:
        print('usage: jvm.py [WKB_JAR_FILE]')
        logging.error('Cannot find WISE KMA Black jar file')
        exit()
        
    wkb_jar_path = sys.argv[1]
    init_jvm(wkb_jar_path=wkb_jar_path)
