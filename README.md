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

## Using

The conversion is a three-step process. First run the script using the component MP3 files as arguments. This will create a JSON file containing metadata for creating the audiobook file.

Second, edit the JSON file as necessary to add/modify the metadata.

Finally, run the script with the JSON file as the sole argument. This will create the audiobook.
