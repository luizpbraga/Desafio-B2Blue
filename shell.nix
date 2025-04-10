with import <nixpkgs> {};
pkgs.mkShell {
  buildInputs = [
    python3
    nodejs
    sqlite
    poetry
  ];
  shellHook = ''
    zsh
  '';
}
