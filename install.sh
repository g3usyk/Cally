rm -rf dist/BL-Cal3D
mkdir dist/BL-Cal3D
cp ./__init__.py dist/BL-Cal3D
cp -r ./src dist/BL-Cal3D
cd ./dist
rm -f BL-Cal3D.zip
zip -r BL-Cal3D.zip BL-Cal3D