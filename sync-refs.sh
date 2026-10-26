# Cleanup
for file in \
    ./skills/*/scripts/* \
    ./skills/*/references/* \
    ; do
rm -v $file
done

# Scripts
for dest in \
    ./skills/*/scripts/ \
    ; do
cp -v ./shared/dossier-renderer ./shared/dossier-validator $dest
done

# grilling.md
for dest in \
    ./skills/prep/references/ \
    ./skills/analysis/references/ \
    ./skills/impl-proposal/references/ \
    ; do
cp -v ./shared/grilling.md $dest
done

# impact-lenses.md
for dest in \
    ./skills/analysis/references/ \
    ./skills/impl-proposal/references/ \
    ; do
cp -v ./shared/impact-lenses.md $dest
done

# caveman.md
for dest in \
    ./skills/prep/references/ \
    ./skills/analysis/references/ \
    ./skills/impl-proposal/references/ \
    ; do
cp -v ./shared/caveman.md $dest;
done
