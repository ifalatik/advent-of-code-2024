# custom module that writes outputs for Advent of Code 2024.

import os
from typing import Any
from ansible.module_utils.basic import AnsibleModule

def run_module() -> None:
    module_args = dict(
        day=dict(type='int', required=True),
        task_number=dict(type='int', required=True),
        result=dict(required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    day: int = module.params['day']
    task_number: int = module.params['task_number']
    result: Any = module.params['result']
    original_file = module.params.get('_original_file', None)

    result_file = f'day{day}_result{task_number}.txt'
    # Check if the 'out' directory exists, if not create it
    result_base_path = os.path.dirname(original_file) if original_file else os.getcwd()
    result_base_path = os.path.join(result_base_path, 'out')
    if not os.path.exists(result_base_path):
        os.makedirs(result_base_path)
    file_path = os.path.join(result_base_path, result_file)

    try:
        with open(file_path, 'w') as file:
            file.write(result)
        module.exit_json(
            changed=True,
            msg=f'result file written successfully: {result_file}'
        )
    except Exception as e:
        module.fail_json(msg=f'Error writing file: {result_file}', exception=str(e))


def main():
    run_module()

if __name__ == '__main__':
    main()
