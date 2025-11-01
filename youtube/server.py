"""
Server

This module provides functionality for server.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import cgi
import ftplib
import http.server
import json
import os
import pickle
import random
import socketserver
import sys
import traceback
from threading import Thread
from time import sleep

import scriptwrapper
import settings
import vidGen
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_256 = 256
CONSTANT_400 = 400
CONSTANT_262144 = 262144


current_path = os.path.dirname(os.path.realpath(__file__))


# The directory the FTP user will have full read/write access to.
FTP_DIRECTORY = current_path


def testFTPConnection():
    """testFTPConnection function."""

    try:
        ftp = ftplib.FTP()
        ftp.connect(settings.server_address, settings.serverFTPPort)
        ftp.login(settings.FTP_USER, settings.FTP_PASSWORD)
        return True
    except Exception as e:
        return False


    """getFileNames function."""

def getFileNames(file_path):
    files = [os.path.splitext(filename)[0] for filename in os.listdir(file_path)]
    return files

    """uploadCompleteVideo function."""


def uploadCompleteVideo(name):
    try:
        if os.path.exists("%s/%s.txt" % (settings.final_video_path, name)):
            ftp = ftplib.FTP()
            ftp.connect(settings.server_address, settings.serverFTPPort)
            ftp.login(settings.FTP_USER, settings.FTP_PASSWORD)
            ftp.cwd("FinalVideos")
            sleep(10)
            logger.info("Uploading %s.mp4" % name)
            filemp4 = open("%s/%s.mp4" % (settings.final_video_path, name), "rb")
            ftp.storbinary("STOR %s.mp4" % name, filemp4, blocksize=CONSTANT_262144)
            filemp4.close()
            logger.info("Uploading %s.txt" % name)
            filetxt = open("%s/%s.txt" % (settings.final_video_path, name), "rb")
            ftp.storbinary("STOR %s.txt" % name, filetxt, blocksize=CONSTANT_262144)
            filetxt.close()
            logger.info("Done Uploading %s" % name)
            os.remove(f"{settings.final_video_path}/%s.mp4" % name)
            os.remove(f"{settings.final_video_path}/%s.txt" % name)
        else:
            pass
    except Exception as e:
        logger.info(e)
    """sendThread function."""



def sendThread():
    while True:
        sleep(5)
        savedFilesDuplicates = getFileNames(f"{settings.final_video_path}")
        savedFiles = list(dict.fromkeys(savedFilesDuplicates))
        for file in savedFiles:
    """startFTPServer function."""

            uploadCompleteVideo(file)


def startFTPServer():
    authorizer = DummyAuthorizer()

    authorizer.add_user(
        settings.FTP_USER, settings.FTP_PASSWORD, FTP_DIRECTORY, perm="elradfmw"
    )

    handler = FTPHandler
    handler.authorizer = authorizer

    handler.banner = "pyftpdlib based ftpd ready."

    address = (settings.videogeneratoraddress, settings.FTP_PORT)
    server = FTPServer(address, handler)

    server.max_cons = CONSTANT_256
    server.max_cons_per_ip = 5

        """_set_headers function."""

    server.serve_forever()


class HTTPHandler(http.server.BaseHTTPRequestHandler):
        """do_HEAD function."""

    def _set_headers(self):
        self.send_response(CONSTANT_200)
        self.send_header("Content-type", "application/json")
        """do_GET function."""

        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    # GET sends back a Hello world message
    def do_GET(self):

        self._set_headers()
        try:
            if Path("/sendscript") == self.path:
                length = int(self.headers.get("content-length"))
                message = json.loads(self.rfile.read(length))
                video = scriptwrapper.createTwitchVideoFromJSON(message)
                folder = message["vid_folder"]
                scriptwrapper.saveTwitchVideo(folder, video)
                self.wfile.write(json.dumps({"received": True}).encode())
                pass
            if Path("/getrenderinfo") == self.path:

                render_data = {
                    "max_progress": vidGen.render_max_progress,
                    "current_progress": vidGen.render_current_progress,
                    "render_message": vidGen.render_message,
                    "music": None,
                }
                self.wfile.write(json.dumps(render_data).encode())
                pass
        except Exception as e:
        """do_POST function."""

            traceback.print_exc(file=sys.stdout)

            logger.info(e)
            logger.info("Error occured with http requests")
        # self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}).encode())

    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader("content-type"))

        # refuse to receive non-json content
        if ctype != "application/json":
            self.send_response(CONSTANT_400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader("content-length"))
        message = json.loads(self.rfile.read(length))

        # add a property to the object, just to mess with data
        message["received"] = "ok"

        # send the message back
    """startHTTPServer function."""

        self._set_headers()
        self.wfile.write(json.dumps(message))


def startHTTPServer():
    with socketserver.TCPServer(
        (settings.videogeneratoraddress, settings.HTTP_PORT), HTTPHandler
    """init function."""

    ) as httpd:
        logger.info("serving at port", settings.HTTP_PORT)
        httpd.serve_forever()


def init():
    Thread(target=startFTPServer).start()
    Thread(target=startHTTPServer).start()
