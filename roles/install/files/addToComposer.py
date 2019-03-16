from __future__ import print_function
import argparse as Args
import json as JSON
import os as OS
import sys as Sys

Parser = Args.ArgumentParser()
Parser.add_argument( '-a', '--toAdd', type=str, required=True )
Parser.add_argument( '-d', '--destination', type=str, required=True )

Args = Parser.parse_args()

def checkDir( Dir, Readable=True, Writeable=False ):
    if OS.path.isdir( Dir ) is False:
        print( "{} not found.".format( Dir ), file=Sys.stderr )
        return False
    return checkAccess( Dir, Readable, Writeable )

def checkFile( File, Readable=True, Writeable=False ):
    if OS.path.isfile( File ) is False:
        print( "{} not found.".format( File ), file=Sys.stderr )
        return False

    return checkAccess( File, Readable, Writeable )

def checkAccess( Path, Readable, Writeable ):
    if True is Readable and OS.access( Path, OS.R_OK ) is False:
        print( "{} is not readable".format( Path ), file=Sys.stderr )
        return False
    if True is Writeable and OS.access( Path, OS.W_OK ) is False:
        print( "{} is not writeable".format( Path ), file=Sys.stderr )
        return False

    return True

if not Args.toAdd.strip():
    Sys.exit( 0 )

if not Args.destination or not checkDir( Args.destination, True, True ):
    Sys.exit( 1 )

ComposerFile = OS.path.join( Args.destination, 'composer.local.json' )

if OS.path.isfile( ComposerFile ):
    if not checkAccess( ComposerFile, True, True ):
        Sys.exit( 1 )

    with open( ComposerFile, 'r' ) as File:
        LocalComposer = File.read()

    LocalComposer = JSON.loads( LocalComposer )
else:
    LocalComposer = {}

ComposerValue = LocalComposer

Pfad = Args.toAdd.split( '||' )

while 2 < len( Pfad ):
    Current = Pfad.pop( 0 )
    if Current not in LocalComposer:
        LocalComposer[ Current ] = {}
    else:
        if not isinstance( LocalComposer[ Current ], dict ):
            print( "There is something wrong with composer.local.json", file=Sys.stderr )
            Sys.exit( 1 )

    LocalComposer = LocalComposer[ Current ]

Current = Pfad.pop( 0 )
if Current not in LocalComposer:
    LocalComposer[ Current ] = []

LocalComposer = LocalComposer[ Current ]

if not isinstance( LocalComposer, list ):
    print( "There is something wrong with composer.local.json", file=Sys.stderr )
    Sys.exit( 1 )

Value = Pfad.pop( 0 )
if Value not in LocalComposer:
    LocalComposer.append( Value )

LocalComposer = JSON.dumps( ComposerValue )

with open( ComposerFile, 'w' ) as File:
    File.write( LocalComposer )

Sys.exit( 0 )
