# Automating Layout Design with PyCell Studio and Custom Compiler for Enhanced Productivity and Efficiency

## Ejecutar
```bash
cd $workdir
export CNI_ROOT=/usr/synopsys/customcompiler/U-2023.03/linux64/PyCellStudio
rm -rf ./Generated/
rm -rf ~/$libreria
cp -r $libreria ~
cngenlib --create --view --techfile $CNI_ROOT/tech/cni130/santanaTech/Santana.tech pkg:$libreria Generated ./Generated

```