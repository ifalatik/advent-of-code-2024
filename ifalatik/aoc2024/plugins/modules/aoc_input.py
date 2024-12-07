# custom module that reads input files for Advent of Code 2024 and stores them in a ansible fact

import os
from ansible.module_utils.basic import AnsibleModule

def run_module() -> None:
    module_args = dict(
        day=dict(type='int', required=True),
        task_number=dict(type='int', required=True),
        single_input=dict(type='bool', required=False, default=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    day: int = module.params['day']
    task_number: int = module.params['task_number']
    single_input: bool = module.params['single_input']
    original_file = module.params.get('_original_file', None)

    if single_input:
        input_file = f'day{day}_input.txt'
    else:
        input_file = f'day{day}_input{task_number}.txt'

    # Resolve search path based on the playbook's location
    search_path = os.path.dirname(original_file) if original_file else os.getcwd()
    search_path = os.path.join(search_path, 'files')
    file_path = os.path.join(search_path, input_file)

    if not os.path.exists(file_path):
        module.fail_json(msg=f"File '{input_file}' not found in '{search_path}'.")

    try:
        out: list[str] = []
        with open(file_path, 'r') as file:
            for line in file:
                out.append(line.strip())

        module.exit_json(
            changed=False,
            msg=f'Input file read successfully: {input_file}',
            ansible_facts={
                f'input_lines_day{day}_task{task_number}': out,
            }
        )
    except FileNotFoundError as e:
        module.fail_json(msg=f'File not found: {input_file}', exception=str(e))
    except Exception as e:
        module.fail_json(msg=f'Error reading file: {input_file}', exception=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()
