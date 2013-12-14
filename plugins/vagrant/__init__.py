
def tasks(tasklist, manifest):
        from pack import VagrantPackages, VagrantConfig
        from pack import VagrantUser, VagrantHostname
        from pack import CreateBox
        tasklist.add(VagrantPackages, VagrantConfig,
                     VagrantHostname, VagrantUser, CreateBox)

def validate_manifest(data, schema_validate):
        from os import path
        schema_path = path.normpath(path.join(path.dirname(__file__), 'manifest-schema.json'))
        schema_validate(data, schema_path)
