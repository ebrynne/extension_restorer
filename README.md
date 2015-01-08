# extension_restorer
A short python script for restoring file extensions to files that have lost theirs. 

I recently was asked by a friend to restore some files from an iTunes backup of her iPhone. Although the backup wasn't encrypted, the original file names and extensions were lost and it would have been a real pain for her to go through every file checking what type of file it was and renaming it accordingly. So I tossed together a version of this script as a quick and dirty way to solve her problem, and then had a little fun generalizing it in case other people might find it handy.

One thing to note is that under certain conditions you may end up with an obscure and poorly documented version of magic. In that case you will get a message about the module having no 'from_file' attribute. At this point you can either fix your version of magic, or make the following two changes to make the script work.

Add these lines at the very start of the main() method:
m = magic.open(magic.MAGIC_MIME)
m.load()

And replace the "ext = ..." line with
ext = mimetypes.guess_extension(m.file(old_file).split(";")[0]

For more information on this problem check out http://stackoverflow.com/questions/25286176/how-to-use-python-magic-5-19-1