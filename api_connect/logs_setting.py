import os
import logging

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
grandparent_dir = os.path.dirname(parent_dir)
files_dir = os.path.join(grandparent_dir, "vending-Flask")
user_count = None
system_log_file_path = os.path.join(files_dir, 'logs', 'logs.log')
actions_log_file_path = os.path.join(files_dir, 'logs', 'actions.log')
error_logs_log_file_path = os.path.join(files_dir, 'logs', 'error_logs.log')
logging.basicConfig(filename=system_log_file_path, level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')


actions_logger = logging.getLogger('actions_log')
actions_logger.setLevel(logging.INFO)
actions_handler = logging.FileHandler(actions_log_file_path)
actions_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
actions_logger.addHandler(actions_handler)


error_logs_logger = logging.getLogger('error_logs_log')
error_logs_logger.setLevel(logging.ERROR)
error_logs_handler = logging.FileHandler(error_logs_log_file_path)
error_logs_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
error_logs_logger.addHandler(error_logs_handler)


system_log_logger = logging.getLogger('system_logs_log')
system_log_logger.setLevel(logging.INFO)
system_log_handler = logging.FileHandler(system_log_file_path)
system_log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
system_log_logger.addHandler(system_log_handler)