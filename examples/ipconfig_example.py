# pylint: disable=missing-module-docstring

from pyconpty import ConPTY

console = ConPTY()
console.run("ipconfig")
print(console.getoutput())
