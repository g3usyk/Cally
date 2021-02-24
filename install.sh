rm -rf dist/*
mkdir dist/BL-Cal3D
cp ./__init__.py dist/BL-Cal3D
cp -r ./src dist/BL-Cal3D
cd ./dist
zip -r BL-Cal3D.zip BL-Cal3D