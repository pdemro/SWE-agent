```bash
python run.py --model_name gpt4 --data_path https://github.com/Das-CPA/demro-cwi-cypress/issues/536 --config_file config/default_from_url.yaml --per_instance_cost_limit 2 --base_commit main --open_pr true
```

```bash
python run.py --model_name gpt4 --data_path https://github.com/Das-CPA/demro-cwi-cypress/issues/536 --config_file config/default_from_url.yaml --per_instance_cost_limit 2 --base_commit main --open_pr true
```

```json
    "program": "${workspaceFolder}/run.py", // Adjust if your main script is named differently
    "console": "integratedTerminal",
    "args": [
    "--model_name",
    "gpt4",
    "--data_path",
    "https://github.com/Das-CPA/demro-cwi-cypress/issues/527",
    "--config_file",
    "config/default_from_url.yaml",
    "--per_instance_cost_limit",
    "2",
    "--base_commit",
    "main",
    "--open_pr",
    "true"
    ],
```
