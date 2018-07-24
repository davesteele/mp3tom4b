# mp3tom4b
Convert mp3 files to an m4b audiobook, with metadata

This can be used, in conjunction with a ripper such as [Sound Juicer](https://wiki.gnome.org/Apps/SoundJuicer),
to convert audiobook CDs to audiobook files.

## Requires

The following are prerequisites:

* Python 3.6 or newer
* ffmpeg
* The Python 3 mutagen module
* MP4Box, from the 'gpac' package

Install the last three with:

    sudo apt-get install ffmpeg python3-mutagen gpac

## Using

The conversion is a three-step process. First run the script using the component MP3 files as arguments. This will create a JSON file containing metadata for creating the audiobook file.

    $ mp3tom4b *.mp3
    metadata saved to "James Herriot's Animal Stories.json"
    $

Second, edit the JSON file as necessary to add/modify the metadata. Specifically, review and update the following fields as required:

* Book "title".
* Book "year", the year of publication.
* Book "coverPath", the path to JPEG or PNG cover art. This can be left blank.
* Book "author".
* The "title" of each chapter.

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

