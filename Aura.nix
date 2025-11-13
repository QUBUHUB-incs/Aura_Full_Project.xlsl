{
  description = "Aura XLSL Paperweb – AI + Spreadsheet Logic + Web Publishing Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    flake-utils.url = "github:numtide/flake-utils";
    dockerTools.url = "github:NixOS/nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, dockerTools, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        # 🐍 Python env for Aura AI + XLSL
        pythonEnv = pkgs.python311.withPackages (ps: with ps; [
          fastapi
          uvicorn
          pandas
          openpyxl
          numpy
          aiohttp
          jinja2
          requests
          psycopg2
          redis
        ]);

        # 🌐 Node.js env for Paperweb frontend
        nodeEnv = pkgs.nodejs_20;

      in {
        # 📦 Package Aura environment
        packages.aura = pkgs.buildEnv {
          name = "aura-xlsl-paperweb";
          paths = [ pythonEnv nodeEnv pkgs.postgresql pkgs.redis ];
        };

        # 🧑‍💻 Dev environment
        devShells.default = pkgs.mkShell {
          name = "aura-dev";
          buildInputs = [
            pythonEnv nodeEnv
            pkgs.git pkgs.postgresql pkgs.redis pkgs.docker-compose
          ];

          shellHook = ''
            echo ""
            echo "🚀 Aura XLSL Paperweb Dev Environment Ready"
            echo "Python: $(python --version)"
            echo "Node: $(node --version)"
            echo "Postgres + Redis available"
            echo ""
          '';
        };

        # 🧠 Run app directly
        apps.default = {
          type = "app";
          program = "${pythonEnv}/bin/uvicorn aura.main:app --host 0.0.0.0 --port 8000";
        };

        # 🐳 Docker image
        packages.dockerImage = pkgs.dockerTools.buildImage {
          name = "aura-xlsl-paperweb";
          tag = "latest";
          config = {
            Cmd = [ "uvicorn" "aura.main:app" "--host" "0.0.0.0" "--port" "8000" ];
            ExposedPorts = { "8000/tcp" = {}; };
            Env = [ "PYTHONUNBUFFERED=1" ];
          };
          contents = [ pythonEnv nodeEnv ];
        };
      });
}
