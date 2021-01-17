import Main
import sys

Main.load_stdlib()
file_name = sys.argv[1]
#check error for reading
print(Main.main(Main.readfile(file_name)))
