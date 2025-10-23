# Force the import of all of the database modules / Tables so that it properly creates them all
from db.print_tracker import PrintTracker
from db.print_file import PrintFile
from db.user_and_role import User, Role
from db.magic_value import MagicValue
