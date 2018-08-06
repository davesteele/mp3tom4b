% mp3tom4b(8)
%
% August 2018

# NAME

**mp3tom4b** - Convert MP3 audio files to an m4b audiobook

## SYNOPSIS

**mp3tom4b** [**-h** | _MP3FILE_ _MP3FILE_ [...] | _JSONFILE_]

## DESCRIPTION

When called with an argument list of MP3 files, **mp3tom4b** will
create a JSON file containing metadata for the collection.

Edit the JSON file to refine meta information for the audiobook.
Specifically, review and update the following fields as required:

  * Book "title".
  * Book "year", the year of publication.
  * Book "coverPath", the path to JPEG or PNG cover art. This can be left blank.
  * Book "author".
  * The "title" of each chapter.

When called with a single argument, **mp3tom4b** will interpret the
argument as a JSON metadata file, and will use it to create a
".m4b" audio file containing the audio and metadata information.

## Options
  **-h**, **--help** - Print help and exit

## See Also
  **rippet**

## COPYRIGHT

**mp3tom4b** is Copyright (C) 2018 David Steele &lt;dsteele@gmail.com&gt;.
