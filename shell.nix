{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; 
    [
      python310
      python310Packages.beautifulsoup4
      tree
      curl
      git
    ];
}
