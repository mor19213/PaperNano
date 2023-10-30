#! /bin/bash
if [ -z "$libreria" ]; then
  echo "libreria variable is not set, exiting script"
  exit 1
fi

if [ -z "$workdir" ]; then
  echo "workdir variable is not set, exiting script"
  exit 1
fi

cd $workdir
export CNI_ROOT=/usr/synopsys/customcompiler/U-2023.03/linux64/PyCellStudio
rm -rf ./GeneratedLib/
#rm -rf ~/$libreria
#cp -r $libreria ~
#cngenlib --create --view --techfile $CNI_ROOT/tech/cni130/santanaTech/Santana.tech pkg:$libreria GeneratedLib ~/GeneratedLib
cngenlib --create --view --techfile /usr/synopsys/iPDK/SAED32nm_PDK_04152022/SAED_PDK_32_28/Santana.tech pkg:$libreria GeneratedLib ./GeneratedLib

rm -rf ~/Desktop/Folder_de_Trabajo/pelmor/*
cp -r GeneratedLib/* ~/Desktop/Folder_de_Trabajo/pelmor/

wait

cd ~/Desktop/Folder_de_Trabajo
custom_compiler