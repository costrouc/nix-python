#include <config.h>
#include <derivations.hh>
#include <globals.hh>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;


PYBIND11_MODULE(_nix, m) {
    m.doc() = R"pbdoc(
        _nix plugin
        -----------------------
        .. currentmodule:: _nix
        .. autosummary::
           :toctree: _generate
           storePathToHash
           isDerivation
    )pbdoc";

    m.def("readDerivation", py::overload_cast<const nix::Path &>(&nix::readDerivation));

    py::class_<nix::Derivation>(m, "Derivation")
      .def_readwrite("outputs", &nix::Derivation::outputs)
      .def_readwrite("inputSrcs", &nix::Derivation::inputSrcs)
      .def_readwrite("platform", &nix::Derivation::platform)
      .def_readwrite("builder", &nix::Derivation::builder)
      .def_readwrite("args", &nix::Derivation::args)
      .def_readwrite("env", &nix::Derivation::env)
      .def("unparse", &nix::Derivation::unparse)
      .def("findOutput", &nix::Derivation::findOutput)
      .def("isFixedOutput", &nix::Derivation::isFixedOutput)
      .def("outputPaths", &nix::Derivation::outputPaths);

    m.def("storePathToHash", &nix::storePathToHash, R"pbdoc(
       Extract the hash part of the given store path
    )pbdoc");

    m.def("isDerivation", &nix::isDerivation, R"pbdoc(
       Determine whether filename is a derivation
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
