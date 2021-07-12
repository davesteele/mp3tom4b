#!/usr/bin/python3
# Copyright (c) 2018 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-3
# License-Filename: LICENSE


import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import textwrap
import xml.etree.ElementTree as ET
from os import R_OK, access
from os.path import isfile
from pathlib import Path
from xml.dom import minidom

from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from unidecode import unidecode


class Book:
    def __init__(self, jsonPath=None):
        for tag in ["title", "coverPath", "year", "author"]:
            setattr(self, tag, "")
        self.chapterList = []

        self.rss_link = ""
        self.rss_desc = ""

        if jsonPath:
            self._LoadJson(jsonPath)

    def _LoadJson(self, jsonPath):
        with open(jsonPath, "r", encoding="utf8") as fp:
            jsonDict = json.load(fp)

        [setattr(self, x, jsonDict[x]) for x in jsonDict if x != "chapters"]

        self.chapterList = []
        for chapDict in jsonDict["chapters"]:
            chapter = Chapter(chapDict["mp3Path"])

            chapter.title = chapDict["title"]

            self.chapterList.append(chapter)

        self.rss_link = jsonDict["rss"]["link"]
        self.rss_desc = jsonDict["rss"]["description"]

    def _SetAttrib(self, tag, value):
        if not getattr(self, tag):
            setattr(self, tag, value)

    def AddChapterMp3(self, path):
        chapter = Chapter(path)
        self.chapterList.append(chapter)

        self._SetAttrib("title", chapter.BookTitle())
        self._SetAttrib("author", chapter.Author())
        self._SetAttrib("year", chapter.Year())

        if not chapter.title:
            chapter.title = "Chapter {}".format(len(self.chapterList))

    def ToJson(self):
        outDict = vars(self).copy()
        del outDict["chapterList"]

        outDict["rss"] = {
            "link": self.rss_link,
            "description": self.rss_desc,
        }

        outDict["chapters"] = [vars(x) for x in self.chapterList]

        return json.dumps(outDict, indent=2)

    def _format_xml(self, element):

        rough_string = ET.tostring(element)
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def Convert(self):
        if self.rss_link or self.rss_desc:
            self.ConvertRss()
        else:
            self.ConvertM4b

    def ConvertRss(self):
        pass
        outputFile = unidecode(self.Title()) + ".rss"
        outputFile = re.sub(" ", "_", outputFile)

        tree = ET.ElementTree("foo")
        # tree.append(ET.Comment("Created by me"))

        rss = ET.Element("rss")
        rss.set("version", "2.0")

        tree._setroot(rss)

        channel = ET.SubElement(rss, "channel")

        title = ET.SubElement(channel, "title")
        title.text = self.title

        link = ET.SubElement(channel, "link")
        link.text = self.rss_link

        desc = ET.SubElement(channel, "description")
        desc.text = self.rss_desc

        image = ET.SubElement(channel, "image")
        iurl = ET.SubElement(image, "url")
        iurl.text = "http://192.168.200.27:8000/" + self.coverPath
        ititle = ET.SubElement(image, "title")
        ititle.text = self.title
        ilink = ET.SubElement(image, "link")
        ilink.text = self.rss_link

        for chapter in self.chapterList:
            item = ET.SubElement(channel, "item")
            chapter.populate_rss_item(item)

        pretty = self._format_xml(rss)
        print(pretty)

        print()

        with open(outputFile, "w", encoding="utf-8") as fp:
            fp.write(pretty)

#         tree.write("/tmp/foo")
#         print()
#         with open("/tmp/foo", "r") as fp:
#             print(fp.read())
        print(f'audiobook saved to "{outputFile}"')


    def ConvertM4b(self):
        outputFile = unidecode(self.Title()) + ".m4b"

        try:
            os.remove(outputFile)
        except OSError:
            pass

        morph = AudioManip()

        aacList = (morph.Mp3ToAac(chap.mp3Path) for chap in self.chapterList)

        morph.ConcatAac(outputFile, aacList, self._ChapterText())

        morph.SetTags(outputFile, self.title, self.author, self.year)

        morph.SetCover(outputFile, self.coverPath)

        print(f'audiobook saved to "{outputFile}"')

    def _ChapterText(self):
        text = ""
        timeStamp = 0

        for (n, title, duration) in zip(
            range(1, len(self.chapterList) + 1),
            [x.title for x in self.chapterList],
            [x.duration for x in self.chapterList],
        ):

            if title:
                seconds = timeStamp
                hours = int(seconds // 3600)
                seconds -= hours * 3600
                minutes = int(seconds // 60)
                seconds -= minutes * 60

                text += f"CHAPTER{n}={hours}:{minutes}:{seconds:.3f}\n"
                text += f"CHAPTER{n}NAME={title}\n"

            timeStamp += duration

        return text

    def Title(self):
        if self.title:
            return self.title

        return "book"


class Chapter:
    def __init__(self, mp3Path, **kwargs):
        self.mp3Path = mp3Path

        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

        mp3 = MP3(self.mp3Path)
        self.duration = mp3.info.length
        self.title = self._GetTag("TIT2")

    def _GetTag(self, tag):
        mp3 = MP3(self.mp3Path)

        try:
            val = mp3[tag].text[0]
        except KeyError:
            val = ""

        return val

    def BookTitle(self):
        return self._GetTag("TALB")

    def Author(self):
        return self._GetTag("TPE1")

    def Year(self):
        return self._GetTag("TORY")

    def populate_rss_item(self, item):
        title = ET.SubElement(item, "title")
        title.text = self.title

        enclosure = ET.SubElement(item, "enclosure")

        enclosure.set("url", "http://192.168.200.27:8000/" + self.mp3Path)
        enclosure.set("length", str(Path(self.mp3Path).stat().st_size))
        enclosure.set("type", "audio/mpeg")


class AudioManip:
    def __init__(self):
        self.tmpdir = tempfile.mkdtemp()

    def __del__(self):
        shutil.rmtree(self.tmpdir)

    def run(self, cmd):
        p = subprocess.Popen(
            shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise Exception(stderr)

    def Mp3ToAac(self, mp3Path):
        aacPath = os.path.join(self.tmpdir, f"{os.path.basename(mp3Path)}.aac")

        cmd = 'ffmpeg -threads 8 -i "{0}" -c:a aac -b:a 64k "{1}"'.format(
            mp3Path, aacPath
        )
        self.run(cmd)
        return aacPath

    def ConcatAac(self, outputFile, inputFiles, chapterText):
        # https://ubuntuforums.org/showthread.php?t=1418085

        tmpOut = tempfile.mktemp(suffix=".m4a", dir=self.tmpdir)

        chapterFile = tempfile.mktemp(suffix=".chaps", dir=self.tmpdir)
        with open(chapterFile, "w", encoding="utf8") as fp:
            fp.write(chapterText)

        for fl in inputFiles:
            cmd = f'MP4Box -cat "{fl}" "{tmpOut}"'
            self.run(cmd)

        cmd = (
            f'MP4Box -add "{tmpOut}" -chap "{chapterFile}" ' f'"{outputFile}"'
        )
        self.run(cmd)

        cmd = f'mp4chaps --convert -Q "{outputFile}"'
        self.run(cmd)

    def SetTags(self, outputFile, title, author, year):
        muMp4 = MP4(outputFile)

        muMp4["\xa9nam"] = title
        muMp4["\xa9alb"] = title
        muMp4["\xa9ART"] = author
        muMp4["\xa9gen"] = "Audiobook"
        muMp4["\xa9day"] = year
        muMp4["\xa9too"] = "Lavc58.35.100"

        muMp4.save()

    def SetCover(self, outputFile, coverPath):
        # https://stackoverflow.com/questions/7275710/mutagen-how-to-detect-and-embed-album-art-in-mp3-flac-and-mp4
        if coverPath:
            audio = MP4(outputFile)
            data = open(coverPath, "rb").read()

            covr = []
            if coverPath.endswith("png"):
                covr.append(MP4Cover(data, MP4Cover.FORMAT_PNG))
            else:
                covr.append(MP4Cover(data, MP4Cover.FORMAT_JPEG))

            audio.tags["covr"] = covr
            audio.save()


def parseArgs():
    parser = argparse.ArgumentParser(
        description="Convert mp3 audio files to an m4b audiobook",
        epilog=textwrap.dedent(
            """
            When called with an argument list of mp3 files, %(prog)s will
            create a JSON file containing metadata for the collection.

            Edit the JSON file to refine meta information for the audiobook.

            When called with a single argument, %(prog)s will interpret the
            argument as a JSON metadata file, and will use it to create an
            m4b audio file containing the mp3 file and metadata information.
            """
        )[1:-1],
        usage="%(prog)s [-h | <MP3 file> <MP3 file> [...] | <JSON file>]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "files",
        nargs="+",
        help=argparse.SUPPRESS,
    )

    args = parser.parse_args()

    for fpath in args.files:
        if not isfile(fpath) or not access(fpath, R_OK):
            parser.print_usage()
            print("{0}: error: {1} not readable".format(sys.argv[0], fpath))
            sys.exit(1)

    if len(args.files) > 1:
        args.mp3_files = args.files
        args.json_file = None
    else:
        args.mp3_files = []
        args.json_file = args.files[0]

    return args


def main():

    args = parseArgs()

    if args.mp3_files:
        book = Book()

        for file in args.mp3_files:
            book.AddChapterMp3(file)

        jname = book.Title() + ".json"

        with open(jname, "w", encoding="utf8") as fp:
            fp.write(book.ToJson())

        print(f'metadata saved to "{jname}"')

    elif args.json_file:
        book = Book(args.json_file)

        book.Convert()



if __name__ == "__main__":
    main()
