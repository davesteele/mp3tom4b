# mp3tom4b
Convert mp3 files to an m4b audiobook, with metadata

This also includes a small CD ripper wrapper, _rippet_, to convert audiobook CDs to MP3 files.

## Requires

The following are prerequisites:

* Python 3.6 or newer
* ffmpeg
* The Python 3 mutagen module
* MP4Box, from the 'gpac' package
* mp4chaps, from the mp4v2-utils package
* cdda2track, from the audiotools package

Install the last five with:

    sudo apt-get install ffmpeg python3-mutagen gpac mp4v2-utils audiotools

Or just install the [deb file](https://davesteele.github.io/mp3tom4b/deb/index.html):

    sudo dpkg -i mp3tom4b*deb
    sudo apt-get -f install

## Using

_rippet_ takes a single argument - the audio CD disk number. It creates MP3 files in the current directory.

The m4b conversion is a three-step process. First run the script using the component MP3 files as arguments. This will create a JSON file containing metadata for creating the audiobook file.

    $ mp3tom4b *.mp3
    metadata saved to "James Herriot's Animal Stories.json"
    $

Second, edit the JSON file as necessary to add/modify the metadata. Specifically, review and update the following fields as required:

* Book "title".
* Book "year", the year of publication.
* Book "coverPath", the path to JPEG or PNG cover art. This can be left blank.
* Book "author".
* The "title" of each chapter. Leave this blank to omit a chapter title for
a particular MP3 file.

Also, re-sort the chapters, if necessary. Note that JSON is a machine-readable format - be careful with the
formatting.

Finally, run the script with the JSON file as the sole argument. This will create the audiobook.

    $ mp3tom4b *json
    audiobook saved to "James Herriot's Animal Stories.m4b"

## Usage

    $ mp3tom4b -h
    usage: mp3tom4b [-h | <MP3 file> <MP3 file> [...] | <JSON file>]
    
    Convert mp3 audio files to an m4b audiobook
    
    optional arguments:
      -h, --help  show this help message and exit
    
    When called with an argument list of mp3 files, mp3tom4b will
    create a JSON file containing metadata for the collection.
    
    Edit the JSON file to refine meta information for the audiobook.
    
    When called with a single argument, mp3tom4b will interpret the
    argument as a JSON metadata file, and will use it to create an
    m4b audio file containing the mp3 file and metadata information.


    $ rippet -h
    usage: rippet [-h] disk_number
    
    Parse a CD to sortable tracks
    
    positional arguments:
      disk_number  disk number
    
    optional arguments:
      -h, --help   show this help message and exit

