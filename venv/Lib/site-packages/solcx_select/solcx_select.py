import types
import solcx
from os import getenv
import sys
from dotenv import load_dotenv
from os import system

load_dotenv()
SOLC_VERSION = getenv("SOLC_VERSION", False)
SOLC_PATH = getenv("SOLC_PATH", getenv("HOME", "~") + "/.local/bin")
# where to make a link for your shell to find the version you want


def setsolc(v):
    try:
        solcx.set_solc_version(v)
        path = solcx.get_solcx_install_folder()
        o = system("ln -sf %s/solc-v%s %s/solc" % (path, v, SOLC_PATH))
        if o == 0:
            print("version set to ", v, "symlink in %s/solc" % (SOLC_PATH,))
        else:
            print("symlink %s/solc failed with nonzero exit status" % (SOLC_PATH,))
    except Exception as e:
        print(e)
        print("using ", solcx.get_solc_version())


def pragma_parse(file):
    fp = open(file, "r")
    dat = fp.readlines()
    for d in dat[0:5]:
        if "pragma" in d:
            return d


def pragma_equip(file):
    pragma = pragma_parse(file)
    try:
        print(pragma)
        solcx.set_solc_version_pragma(pragma)
        print("using ", solcx.get_solc_version())
    except:
        print("installing")
        solcx.install_solc_pragma(pragma)
        print("installed")
        solcx.set_solc_version_pragma(pragma)
        print("using ", solcx.get_solc_version())


alias_latest = ["latest"]
alias_install = ["install", "add"]
alias_v = ["show", "version", "get", "using"]
alias_ls = ["ls", "versions", "installed"]
alias_set = ["set", "use"]
alias_get_solcx_path = ["solcx_path", "which"]
alias_ls_installable = ["bin", "installable", "lsbin", "available", "list"]
alias_solc_path = ["link", "solc_path", "path"]
alias_compile = ["build", "compile"]
alias_compilable = ["sources", "compilable", "buildable", "src"]
alias_pragma = ["pragma", "equip", "for"]
funz = [
    "compile_solc",
    "get_compilable_solc_versions",
    "get_installable_solc_versions",
    "get_installed_solc_versions",
    "get_solc_version",
    "get_solcx_install_folder",
    "install_solc",
    "install_solc_pragma",
    "set_solc_version",
    "set_solc_version_pragma",
]


def help():
    print("solcx-select [cmd] [arg]", "\n")
    print(
        "solcx-select adds version of solc selected by solcx to your shell path", "\n"
    )
    print(
        "if SOLC_VERSION is set, it will set this version if given no other command",
        "\n",
    )

    print(str(alias_install), " - installs version(s) supplied")
    print(str(alias_v), " - display current version")
    print(str(alias_ls), " - show versions installed/available")
    print(str(alias_set), "  - set version")
    print(
        str(alias_pragma),
        "  <file.sol>",
        " read pragma from contract, set compliant version as specified, install if needed",
    )
    print(str(alias_compilable), "  - get list of compilable versions")
    print(str(alias_compile), "  - install from source")
    print(str(alias_get_solcx_path), "  - get path to solcx binaries")
    print(str(alias_ls_installable), "  - list versions available to install")
    print(
        str(alias_solc_path),
        "  - path to solc symlink, set by env var SOLC_PATH defaulting to ~/.local/bin",
        "\n",
    )


def main():
    argvx = sys.argv[1::]
    if len(argvx) > 0:
        cmd = argvx[0].lower()
        if cmd in alias_install:
            try:
                print("installing...")
                for a in argvx[1::]:
                    solcx.install_solc(a)
                    print("installed ", a)
            except Exception as e:
                print(e)
        elif cmd in alias_v:
            print(solcx.get_solc_version())
        elif cmd in alias_ls:
            for ve in solcx.get_installed_solc_versions():
                print(getattr(ve, "base_version", str(ve)))
        elif cmd in alias_ls_installable:
            for ve in solcx.get_installable_solc_versions():
                print(getattr(ve, "base_version", str(ve)))
        elif cmd in alias_set:
            setsolc(argvx[1])
        elif cmd in alias_get_solcx_path:
            print(str(solcx.get_solcx_install_folder()))
        elif cmd in alias_solc_path:
            print(SOLC_PATH)
        elif cmd in alias_pragma:
            pragma_equip(argvx[1])
        elif cmd in alias_compile:
            for a in argvx[1::]:
                print("compiling...,", a)
                solcx.compile_solc(a)
        elif cmd in alias_compilable:
            for ve in solcx.get_compilable_solc_versions():
                print(getattr(ve, "base_version", str(ve)))
        elif cmd in alias_latest:
            s = solcx.get_installable_solc_versions()
            s.sort(reverse=True)
            if s[0] in solcx.get_installed_solc_versions():
                setsolc(s[0].base_version)
            else:
                solcx.install_solc(s[0].base_version)
                setsolc(s[0].base_version)
        else:
            help()
    elif SOLC_VERSION:
        try:
            setsolc(SOLC_VERSION)
        except:
            print("unknown solc version ", SOLC_VERSION)
            help()
    else:
        help()
        print(solcx.get_solc_version())
