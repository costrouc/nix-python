#include <string>

#include <config.h>
#include <derivations.hh>
#include <globals.hh>
#include <profiles.hh>
#include <store-api.hh>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

nix::Hash hashDerivation(nix::Derivation derivation) {
  nix::initPlugins();
  auto store = nix::openStore();
  auto hash = nix::hashDerivationModulo(*store, derivation);
  return hash;
}


nix::Settings getSettings() {
  return nix::settings;
}


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

    // =========== SETTINGS ============
    // globals.hh

    m.def("settings", &getSettings);

    py::class_<nix::Settings>(m, "Settings")
      .def_readwrite("nix_prefix", &nix::Settings::nixPrefix)
      .def_readwrite("nix_store", &nix::Settings::nixStore)
      .def_readwrite("nix_data_dir", &nix::Settings::nixDataDir)
      .def_readwrite("nix_log_dir", &nix::Settings::nixLogDir)
      .def_readwrite("nix_state_dir", &nix::Settings::nixStateDir)
      .def_readwrite("nix_conf_dir", &nix::Settings::nixConfDir);

    // ========== DERIVATIONS ==========
    // derivations.hh

    m.def("readDerivation", py::overload_cast<const nix::Path &>(&nix::readDerivation));

    m.def("hashDerivation", &hashDerivation);

    py::class_<nix::Derivation>(m, "Derivation")
      .def_readwrite("outputs", &nix::Derivation::outputs)
      .def_readwrite("inputSrcs", &nix::Derivation::inputSrcs)
      .def_readwrite("inputDrvs", &nix::Derivation::inputDrvs)
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

    // ============= HASH ==============
    // hash.hh

    py::class_<nix::Hash>(m, "Hash")
      .def("to_string", &nix::Hash::to_string);

    py::enum_<nix::Base>(m, "Base")
      .value("Base64", nix::Base::Base64)
      .value("Base32", nix::Base::Base32)
      .value("Base16", nix::Base::Base16)
      .value("SRI", nix::Base::SRI)
      .export_values();

    // ========== PROFILES =============
    // profiles.hh

    m.def("findGenerations", &nix::findGenerations);

    py::class_<nix::Generation>(m, "Generation")
      .def_readonly("number", &nix::Generation::number)
      .def_readonly("path", &nix::Generation::path)
      .def_readonly("creationTime", &nix::Generation::creationTime);

    // ========== STORE API ============
    // store-api.hh

    // py::class_<nix::Store>(m, "Store")
    //   .def("is_in_store", &nix::Store::isInStore);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
