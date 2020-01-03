from _nix import isDerivation, storePathToHash, readDerivation


def test_create_derivation():
    # createDerivation('asdfasdf')
    assert True


def test_not_derivation():
    assert not isDerivation('/nix/store/6i15dfg29dh66d9l532iv3hj5x6rx9xy-python3.7-nixpkgs-python-0.0.1dev')


def test_store_path_to_hash():
    assert storePathToHash('/nix/store/6i15dfg29dh66d9l532iv3hj5x6rx9xy-python3.7-nixpkgs-python-0.0.1dev') == "6i15dfg29dh66d9l532iv3hj5x6rx9xy"


def test_isderivation():
    assert not isDerivation('Derive([("out","/nix/store/n214akq42as1ckzj605c3s6y42cxby02-hello-2.10","","")],[("/nix/store/g06lcsnffbn2pqr9jlyrd3jr05ysvzqp-stdenv-linux.drv",["out"]),("/nix/store/i7bl3bw4xll9zsijhj619s3sj6ikra4k-hello-2.10.tar.gz.drv",["out"]),("/nix/store/nn8gylhzg8ba3i1i94kdlirayj7jqfhm-bash-4.4-p23.drv",["out"])],["/nix/store/9krlzvny65gdc8s7kpb6lkx8cd02c25b-default-builder.sh"],"x86_64-linux","/nix/store/wd1jazzawjk4w1d31ism7fm7vdg4ma9l-bash-4.4-p23/bin/bash",["-e","/nix/store/9krlzvny65gdc8s7kpb6lkx8cd02c25b-default-builder.sh"],[("buildInputs",""),("builder","/nix/store/wd1jazzawjk4w1d31ism7fm7vdg4ma9l-bash-4.4-p23/bin/bash"),("configureFlags",""),("depsBuildBuild",""),("depsBuildBuildPropagated",""),("depsBuildTarget",""),("depsBuildTargetPropagated",""),("depsHostHost",""),("depsHostHostPropagated",""),("depsTargetTarget",""),("depsTargetTargetPropagated",""),("doCheck","1"),("doInstallCheck",""),("name","hello-2.10"),("nativeBuildInputs",""),("out","/nix/store/n214akq42as1ckzj605c3s6y42cxby02-hello-2.10"),("outputs","out"),("patches",""),("pname","hello"),("propagatedBuildInputs",""),("propagatedNativeBuildInputs",""),("src","/nix/store/3x7dwzq014bblazs7kq20p9hyzz0qh8g-hello-2.10.tar.gz"),("stdenv","/nix/store/fiaj00zrmb7dynd2q9xmcrh5rn0mjwj0-stdenv-linux"),("strictDeps",""),("system","x86_64-linux"),("version","2.10")])')
