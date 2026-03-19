module.exports = {
  apps: [
    {
      name: "api-report-giro-cama",
      cwd: __dirname,

      script: ".venv/bin/python",
      args: "-m uvicorn src.main:app --host 127.0.0.1 --port 4000",

      interpreter: "none",
      exec_mode: "fork",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "500M",

      env: {
        APP_ENV: "production",
        PYTHONIOENCODING: "utf-8",
      },
    },
  ],
};
