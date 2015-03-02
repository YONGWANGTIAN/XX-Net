import os
import sys
import platform
import shutil
import logging
import time

current_path = os.path.dirname(os.path.abspath(__file__))
python_path = os.path.abspath( os.path.join(current_path, os.pardir, os.pardir, 'python27', '1.0'))

def copy_VCR_files():
    src_path = os.path.join(python_path, "WinSxS")
    win_path = os.environ['WINDIR']
    win_dst_path = os.path.join(win_path, "WinSxS")

    for path, dirs, files in os.walk(src_path):
        for file in files:
            sep_path = path.split(os.path.sep)
            relate_path = os.path.sep.join(sep_path[5:])
            #print relate_path
            dest_path = os.path.join(win_dst_path, relate_path)
            if not os.path.isdir(dest_path):
                logging.info("setup win python, mkdir:%s", dest_path)
                os.mkdir(dest_path)
            #print "root:", path
            #print "file:", file
            src_path = os.path.join(path, file)
            target_file = os.path.join(dest_path, file)
            if not os.path.isfile(target_file):
                logging.info("setup win python, copy:%s %s", src_path, target_file)
                shutil.copyfile(src_path, target_file)

def is_winxp():
    if sys.platform != "win32":
        return False
    if platform.release() != "XP":
        return False
    return True

def check_setup(): #40ms
    if is_winxp():
        try:
            copy_VCR_files()
        except Exception as e:
            logging.exception("setup win python except:%s", e)

def smart_check(): #400 ms
    import uuid
    node_id = uuid.getnode()
    import config
    config.load()

    if current_path != config.config["update"]["last_path"] or node_id != config.config["update"]["node_id"]:
        check_setup()

if __name__ == "__main__":
    t1 = time.time()
    check_setup()
    t2 = time.time()
    t_c = (t2 - t1) * 1000
    print "cost time:", t_c
