#! /bin/bash

cd $workdir
export CNI_ROOT=/usr/synopsys/customcompiler/U-2023.03/linux64/PyCellStudio
rm -rf ~/GeneratedLib/
rm -rf ~/$libreria
cp -r $libreria ~
cngenlib --create --view --techfile $CNI_ROOT/tech/cni130/santanaTech/Santana.tech pkg:$libreria GeneratedLib ~/GeneratedLib

wait
custom_compiler