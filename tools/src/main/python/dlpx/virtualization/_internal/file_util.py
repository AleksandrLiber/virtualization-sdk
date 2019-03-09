#
# Copyright (c) 2019 by Delphix. All rights reserved.
#

import logging
import os
import shutil
import traceback

from dlpx.virtualization._internal import exceptions

logger = logging.getLogger(__name__)


def delete_paths(*args):
    """
    Does best effort cleanup of the given paths. Exceptions are logged
    and not raised.

    Directories are recursively deleted.

    Args:
        args (list of str): A list of paths to attempt to delete.
    """
    for path in args:
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    logger.debug(
                        'A directory exists at %r. Attempting to delete.',
                        path)
                    shutil.rmtree(path)
                else:
                    logger.debug('A file exists at %r. Attempting to delete.',
                                 path)
                    os.remove(path)
            except Exception as e:
                logger.debug('Failed to delete %r: %s.', path, e.message)
                logger.debug(traceback.format_exc())


def validate_paths_do_not_exist(*args):
    """
    Validates the given file paths do not exist.

    Args:
        args (list of str): A list of paths to validate they do not exist.
    Raises:
        PathExistsError: If any of the provided paths already exist.
    """
    logger.info('Validating files and directories to be written do not exist.')
    for path in args:
        if os.path.exists(path):
            raise exceptions.PathExistsError(path)
        logger.debug('SUCCESS: Path %r does not exist.', path)
