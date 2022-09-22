{ lib, python3Packages, python3 }:

with python3Packages;

buildPythonApplication rec {
  pname = "moses";
  version = "0.1";

  src = ./.;

  propagatedBuildInputs = [
    pikepdf
    click
  ];

  doCheck = false;

  meta = with lib; {
    homepage = "https://github.com/riotbib/moses";
    description = "Splitting PDF files into chunks. ";
    license = licenses.bsd3;
    maintainers = with maintainers; [ fridh ];
  };
}
