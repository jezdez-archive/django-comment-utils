"""
A script which removes spam comments from the database.

The determination of which comments are spam is based on two pieces of
information:

1. The comment's ``is_public`` field, and

2. The comment's age.

If the ``is_public`` field is set to ``False`` and the comment is
older than a specified threshold (see below), it will be considered
spam and will be deleted.

**Arguments:**

``-a``, ``--age=AGE``
    The age threshold, in days, past which a non-public comment will
    be considered spam, and thus deleted. Defaults to 14 if not
    supplied (and thus will delete non-public comments which are at
    least two weeks old).

``-d``, ``--dry-run``
    Does not delete any comments, but merely prints the number of
    comments which would have been deleted.

``-s``, ``--settings=SETTINGS``
    Django settings module to use. This argument is required.

``-v``, ``--verbose``
    Run verbosely, printing information to standard output about each
    comment as it is deleted.

Regardless of the ``verbose``flag, this script will print the total
number of deleted comments to standard output when finished.

This script is intended to be run as a cron job; for example, to have
it run at midnight each Sunday, with default values::

    0 0 * sun python /path/to/comment_utils/bin/delete_spam_comments.py --settings=yoursite.settings

"""

import os
from optparse import OptionParser
from django.core import management

if __name__ == '__main__':
    usage = "usage: %prog --settings=settings [options]"
    parser = OptionParser(usage)
    parser.add_option('-a', '--age', dest='age', metavar='AGE', type='int',
                      help="The age threshold, in days, past which a non-public comment will be considered spam, and thus be deleted. Defaults to 14 if not supplied.")
    parser.add_option('-d', '--dry-run', action="store_true", dest="dry_run",
                      help="Does not delete any comments, but merely outputs the number of comments which would have been deleted.")
    parser.add_option('-s', '--settings', dest='settings', metavar='SETTINGS',
                      help="Django settings module to use. This argument is required.")
    parser.add_option('-v', '--verbose', dest='verbose', metavar='VERBOSE', action='store_true',
                      help="Run verbosely, printing information to standard output about each comment as it is deleted.")
    (options, args) = parser.parse_args()
    if not options.settings:
        parser.error("You must specify a settings module.")
    os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
    age = options.age or 14
    dry_run = options.dry_run or False
    verbose = options.verbose or False

    if verbose:
        verbosity = 2
    else:
        verbosity = 1
    management.call_command('delete_spam_comments', age=age, dry_run=dry_run, verbosity=verbosity)
