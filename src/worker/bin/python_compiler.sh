#! /bin/bash
echo "#!/usr/bin/python" > ../compiled_executables/$2;
cat ../src_code/$1 >> ../compiled_executables/$2;
chmod 777 ../compiled_executables/$2
