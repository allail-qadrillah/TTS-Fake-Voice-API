import json

def load_json(path):
  file = open( path, 'r' )
  return json.loads( file.read() )