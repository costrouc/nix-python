{ pkgs ? import <nixpkgs> { }, pythonPackages ? pkgs.python3Packages }:

pythonPackages.buildPythonPackage rec {
  pname = "nixpkgs-python";
  version = "0.0.1dev";

  src = ./.;

  postPatch = ''
    substituteInPlace setup.py \
      --replace "/usr/include/nix" "${pkgs.nix.dev}/include/nix" \
      --replace "library_dirs=[]," "library_dirs=['${pkgs.nix}/lib'],"
  '';

  buildInputs = [
    pkgs.nix
    pythonPackages.pybind11
    pkgs.boost
  ];

  propagatedBuildInputs = [

  ];

  checkInputs = [
    pythonPackages.pytest
  ];

  checkPhase = ''
    pushd dist
    pytest ../tests
    popd
  '';
}
