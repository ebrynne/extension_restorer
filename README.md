# Extension Restorer
## Summary
A short python script for restoring file extensions to files that have lost theirs. 

## Backstory
I recently was asked by a friend to restore some files from an iTunes backup of her iPhone. Although the backup wasn't encrypted, the original file names and extensions were lost and it would have been a real pain for her to go through every file checking what type of file it was and renaming it accordingly. So I tossed together a version of this script as a quick and dirty way to solve her problem, and then had a little fun generalizing it in case other people might find it handy.

## Usage
usage: extension_restorer.py [-h] [-s SOURCE] [-t TARGET] [-v]
                             [--root_name ROOT_NAME] [--minsize MINSIZE]
                             [--blacklist [BLACKLIST [BLACKLIST ...]]]
                             [--whitelist [WHITELIST [WHITELIST ...]]]

Autodetect file encoding and add appropriate file extension

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        The source directory to process (defaults to working
                        directory
  -t TARGET, --target TARGET
                        The target output directory (defaults to working
                        directory)
  -v, --verbose         PRINT EVERYTHING!
  --root_name ROOT_NAME
                        Each file will be named <ROOT_NAME>_<NUMBER>.<EXT>. If
                        root_name is not specified the generated extension is
                        just added to the existing filename
  --minsize MINSIZE     Exlude files less than this number of bytes.
  --blacklist [BLACKLIST [BLACKLIST ...]]
                        A list of extensions to exclude. Any files that are
                        determined to require these extensions will not be
                        written.
  --whitelist [WHITELIST [WHITELIST ...]]
                        A list of extensions to include. Only files that are
                        determined to require these extensions will be
                        written. If both a blacklist and a whitelist are
                        specified, the whitelist will be respected.

Ex. ./pic_extractor.py --target ~/recovered_photos -v --root_name photo
--minsize=25000 --whitelist png jpg

## Common errors
##### 'module' object has no attribute 'from_file'
One thing to note is that under certain conditions you may end up with an obscure and poorly documented version of magic. In that case you will get a message about the module having no 'from_file' attribute. At this point you can either fix your version of magic, or make the following two changes to make the script work.

Add these lines at the very start of the main() method:
m = magic.open(magic.MAGIC_MIME)
m.load()

And replace the "ext = ..." line with
ext = mimetypes.guess_extension(m.file(old_file).split(";")[0]

For more information on this problem check out http://stackoverflow.com/questions/25286176/how-to-use-python-magic-5-19-1