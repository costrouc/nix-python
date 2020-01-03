let pkgs = import (builtins.fetchTarball {
      url = "https://github.com/NixOS/nixpkgs/archive/613fa47c464bf3782ef65212ee38499f84946e95.tar.gz";
      sha256 = "11lg18zpzrpd6i3ivny4wn1f51xs1aynkhgdkjpx5m4ff63i0aq8";
    }) { };

    pythonPackages = pkgs.python3Packages;

    nix-python = import ./build.nix { inherit pkgs pythonPackages; };
in
pkgs.mkShell {
  buildInputs = [
    nix-python
    pythonPackages.requests
    pythonPackages.diskcache
    pythonPackages.brotli
    pythonPackages.pythonix
    pythonPackages.pytest
    pythonPackages.pybind11
    pkgs.graphviz
    pkgs.nix
  ];

  shellHook = ''

  '';

}
