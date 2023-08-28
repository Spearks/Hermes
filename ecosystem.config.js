module.exports = {
    apps: [
      {
        name: "beat",
        cwd: ".",
        script: "/root/.cache/pypoetry/virtualenvs/hermes-ILN3loXx-py3.10/bin/python3",
        args:
          "-m celery -A hermes worker --loglevel=INFO",
        watch: true,
        interpreter: "",
        max_memory_restart: "1G"
      },
      {
        name: "worker",
        cwd: ".",
        script: "/root/.cache/pypoetry/virtualenvs/hermes-ILN3loXx-py3.10/bin/python3",
        args: "-m celery -A hermes beat --loglevel=INFO",
        watch: true,
        interpreter: "",
        max_memory_restart: "1G"
      },
      {
        name: "runner",
        cwd: ".",
        script: "/root/.cache/pypoetry/virtualenvs/hermes-ILN3loXx-py3.10/bin/python3",
        args: "manage.py runserver 41000",
        watch: true,
        interpreter: "",
        max_memory_restart: "1G"
      },
      {
        name: "export dummy",
        cwd: ".",
        script: "/root/.cache/pypoetry/virtualenvs/hermes-ILN3loXx-py3.10/bin/python3",
        args: "export_dummy.py",
        watch: true,
        interpreter: "",
        max_memory_restart: "1G"
      },
      {
        name: "export",
        cwd: ".",
        script: "/root/.cache/pypoetry/virtualenvs/hermes-ILN3loXx-py3.10/bin/python3",
        args: "export.py",
        watch: true,
        interpreter: "",
        max_memory_restart: "1G"
      }
    ]
  };