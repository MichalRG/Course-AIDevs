from typing import Dict


def load_env_variables(env_name_file = ".env") -> Dict[str, str]:
  try:
    with open(env_name_file) as file:
      variables_dict = {}

      for line in file:
        stripped_line = line.strip()

        if stripped_line.startswith("#") or not line:
          continue

        key, value = line.split("=",1)

        variables_dict[key] = value
      
      return variables_dict

  except FileNotFoundError:
    print(f"ERROR: {env_name_file} not found")
    return {}