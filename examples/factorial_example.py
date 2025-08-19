# pylint: disable=missing-module-docstring

from pyconpty import ConPTY

console = ConPTY()
console.run("factorial.exe", stripinput=True)
number = input(console.getoutput())

if number[0] == "-":
    number_without_minus = number[1:]
else:
    number_without_minus = number

if number_without_minus.isdigit():
    console.sendinput(str(number))
    print(console.getoutput())
else:
    print(" Only integer numbers accepted!\n")

if console.isrunning:
    console.kill()
