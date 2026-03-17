module.exports = {
  apps: [
    {
      name: "api-report-giro-cama",
      cwd: __dirname,
      script: "python3",
      args: "-m uvicorn src.main:app --host 0.0.0.0 --port 8000",
      interpreter: "none",
      exec_mode: "fork",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "500M",
      env: {
        APP_ENV: "development",
        APP_PORT: 8000,
        PYTHONIOENCODING: "utf-8", // <-- agrega esto
      },
      env_production: {
        APP_ENV: "production",
        APP_PORT: 8000,
        PYTHONIOENCODING: "utf-8", // <-- agrega esto
      },
    },
  ],
};
