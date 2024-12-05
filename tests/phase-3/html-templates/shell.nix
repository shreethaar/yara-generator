{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.nodejs
    pkgs.yarn  # Optional if you prefer yarn over npm
  ];

  shellHook = ''
    echo "Welcome to the React development environment!"
    echo "Run 'npm install' to install dependencies for your React app."
  '';
}

