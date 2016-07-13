
import ConfigParser
# import io

CONFIG_FILE_PATH = "../conf/app.cfg"

config = ConfigParser.ConfigParser(allow_no_value=True)
config.read(CONFIG_FILE_PATH)
db_type  = config.get("database", "type")
user = config.get("database", "user")
password = config.get("database", "password")
uri = config.get("database", "uri")

db_uri = db_type + "://" + user + ":" + password + "@" + uri
print(db_uri)