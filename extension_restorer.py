#!/usr/bin/env python
import magic
import os
import md5
import mimetypes
import shutil
import sys
import argparse

parser = argparse.ArgumentParser(description="Autodetect file encoding and add appropriate file extension",
  epilog="Ex. ./pic_extractor.py --target ~/recovered_photos -v --root_name photo --minsize=25000 --whitelist png jpg")
parser.add_argument('-s', '--source', default='.', help="The source directory to process (defaults to working directory")
parser.add_argument('-t', '--target', default='.', help="The target output directory (defaults to working directory)")
parser.add_argument('-v', '--verbose', action='store_true', help="PRINT EVERYTHING!")
parser.add_argument('--root_name', default='', help="Each file will be named <ROOT_NAME>_<NUMBER>.<EXT>. If root_name is not specified the generated extension is just added to the existing filename")
parser.add_argument('--minsize', type=int, default=0, help="Exlude files less than this number of bytes.")
parser.add_argument('--blacklist', default=[], nargs='*', help="A list of extensions to exclude. Any files that are determined to require these extensions will not be written.")
parser.add_argument('--whitelist', default=[], nargs='*', help="A list of extensions to include. Only files that are determined to require these extensions will be written. If both a blacklist and a whitelist are specified, the whitelist will be respected.")
opts = parser.parse_args(sys.argv[1:])

ext_aliases = {
  ".jpe": [".jpeg", ".jif", ".jpg"]
}

multi_version_exts = {i: k for k, v in ext_aliases.items() for i in v}

def main(ext_map, source, target):
  written_files = set()
  file_count = len(os.listdir(source))
  skipped_file_count = 0
  error_file_count = 0
  for i, file_name in enumerate(os.listdir(source)):
    try:
      old_file = "{0}{1}".format(source, file_name)
      ext = mimetypes.guess_extension(magic.from_file(old_file, mime=True).split(";")[0])
      if should_include_extension(ext, ext_map) and os.stat(old_file).st_size > opts.minsize:
        ext = ext_aliases[ext][0] if ext in ext_aliases else ext
        m = md5.new()
        m.update(open(old_file).read())
        file_hash = m.digest()
        if file_hash not in written_files:
          new_name = "{0}_{1}".format(opts.root_name, i) if opts.root_name else file_name
          new_file = "{0}{1}{2}".format(target, new_name, ext)
          if target == '.' and file_name == new_name:
            os.rename(f, new_file)
          else:
            shutil.copyfile(old_file, new_file)
          written_files.add(file_hash)
          verbose_print("%s / %s" % (i, file_count))
        else:
          skipped_file_count += 1
    except Exception as e:
      verbose_print("Error processing file: {0}".format(file_name))
      verbose_print(e)
      error_file_count += 1

  print "Processed {0} files".format(file_count)
  print "Wrote {0} files".format(len(written_files))
  print "Errors with {0} files".format(error_file_count)
  verbose_print("Skipped {0} duplicates".format(skipped_file_count))

def should_include_extension(ext, ext_map):
  if ext:
    if opts.whitelist:
      return ext in ext_map
    else:
      return ext not in ext_map
  else:
    return False

def normalize_exts(exts):
  ext_map = dict(map(
    lambda ext: ((ext if ext.startswith(".") else ".{0}".format(ext)).lower(), None),
    exts
  ))
  print ext_map
  print multi_version_exts
  # guess_extension returns '.jpe' for jpegs, which no one wants/will think to filter for.
  # If the user has selected to filter any jpeg extension, filter  '.jpe', otherwise map '.jpe' to '.jpeg'
  for e in set(multi_version_exts.keys()).intersection(set(ext_map.keys())):
    ext_map[multi_version_exts[e]] = None
  return ext_map

def normalize_path(path):
  return "{0}/".format(path) if path and not path.endswith('/') else path

def verbose_print(str):
  if opts.verbose:
    print str

# Prefer whitelist
ext_map = normalize_exts(opts.whitelist) if opts.whitelist else normalize_exts(opts.blacklist)

# Make sure there's a trailing slash on the output path
source = normalize_path(opts.source)
target = normalize_path(opts.target)


if __name__ == "__main__":
  main(ext_map, source, target)