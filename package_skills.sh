./sync-refs.sh

cd ./skills

for skill in *; do
    zip -r $skill.zip $skill/*
done

mv -v *.zip ../export
cd ..
