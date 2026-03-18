module.exports = {
  apps: [
    {
      name: "api-report-giro-cama",
      cwd: __dirname,

      script: ".venv/bin/python",
      args: "-m uvicorn src.main:app --host 0.0.0.0 --port 443 --ssl-certfile /home/rpatic/ssl/server-cert.pem --ssl-keyfile /home/rpatic/ssl/server-key.pem",

      interpreter: "none",
      exec_mode: "fork",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "500M",

      env: {
        APP_ENV: "production",
        APP_PORT: 443,
        PYTHONIOENCODING: "utf-8",
      },
    },
  ],
};
