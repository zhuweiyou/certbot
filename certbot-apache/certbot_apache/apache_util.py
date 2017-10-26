""" Utility functions for certbot-apache plugin """
import os

def get_mod_deps(mod_name):
    """Get known module dependencies.

    .. note:: This does not need to be accurate in order for the client to
        run.  This simply keeps things clean if the user decides to revert
        changes.
    .. warning:: If all deps are not included, it may cause incorrect parsing
        behavior, due to enable_mod's shortcut for updating the parser's
        currently defined modules (`.ApacheParser.add_mod`)
        This would only present a major problem in extremely atypical
        configs that use ifmod for the missing deps.

    """
    deps = {
        "ssl": ["setenvif", "mime"]
    }
    return deps.get(mod_name, [])


def get_file_path(vhost_path):
    """Get file path from augeas_vhost_path.

    Takes in Augeas path and returns the file name

    :param str vhost_path: Augeas virtual host path

    :returns: filename of vhost
    :rtype: str

    """
    if not vhost_path or not vhost_path.startswith("/files/"):
        return None

    return _split_aug_path(vhost_path)[0]


def get_internal_aug_path(vhost_path):
    """Get the Augeas path for a vhost with the file path removed.

    :param str vhost_path: Augeas virtual host path

    :returns: Augeas path to vhost relative to the containing file
    :rtype: str

    """
    return _split_aug_path(vhost_path)[1]


def _split_aug_path(vhost_path):
    """Splits an Augeas path into a file path and an internal path.

    After removing "/files", this function splits vhost_path into the
    file path and the remaining Augeas path.

    :param str vhost_path: Augeas virtual host path

    :returns: file path and internal Augeas path
    :rtype: `tuple` of `str`

    """
    # Strip off /files
    file_path = vhost_path[6:]
    internal_path = []

    # Remove components from the end of file_path until it becomes valid
    while not os.path.exists(file_path):
        file_path, _, internal_path_part = file_path.rpartition("/")
        internal_path.append(internal_path_part)

    return file_path, "/".join(reversed(internal_path))


