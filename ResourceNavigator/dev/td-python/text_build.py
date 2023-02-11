from datetime import datetime

build_destination = "../release"
build_name = "td_navigator"
build_version = str("0.0.6")
build_log = op('text_build_log')
build_buffer = op('/sys/quiet')

def get_time():
    return datetime.now()

def version(**kwargs):
    tox_version = kwargs.get('tox_version')
    target_tox = kwargs.get('target_tox')

    target_tox.par.Tdversion = project.saveVersion
    append_log(f"Setting TD Version {project.saveVersion}")
    
    target_tox.par.Tdbuild = project.saveBuild
    append_log(f"Setting TD Build {project.saveBuild}")
    
    target_tox.par.Toxversion = tox_version
    append_log(f"Setting TD Version {tox_version}")

def save_build_and_quit(path):
    '''
    '''
    self._log(f"Saving build to : {path}")
    project.save(path)
    self._log(f"Quitting Source Project")
    project.quit(force=True)
    pass

def find_external_ops(source_op):
    '''
    '''
    external_DATs = source_op.findChildren(type=DAT)
    synced_ops = [eachOp for eachOp in external_DATs if eachOp.par['syncfile'] != None]

    return synced_ops

def turn_off_sync_and_clear_file_DATs(synced_ops):
    '''
    '''
    append_log(f"Turning off sycned DATs")
    for each_op in synced_ops:
        if each_op.par.syncfile:
            each_op.par.file = ''
            each_op.par.syncfile = False
            append_log(f"- - >DAT : {each_op}")
        else:
            pass

def build():
    '''
    '''
    # clear the previous build log
    build_log.clear()

    append_log(f"Build processes initiated")

    append_log(f"Copy TOX to buffer")
    tox_copy = build_buffer.copy(parent())
    tox_copy.nodeX = 0
    tox_copy.nodeY = 200

    # turn off sync and clear file path
    external_ops = find_external_ops(tox_copy)
    turn_off_sync_and_clear_file_DATs(external_ops)

    # set version info
    version(tox_version=build_version, target_tox=tox_copy)

    output_file = f"{tdu.expandPath(build_destination)}/{build_name}.tox"
    tox_copy.save(output_file, createFolders=True)
    
    # clean up buffer
    tox_copy.destroy()

    append_log("Build complete")

def append_log(msg):
    log_msg = f"{get_time()} | {msg}"
    print(log_msg)
    print(log_msg, file=build_log)

build()